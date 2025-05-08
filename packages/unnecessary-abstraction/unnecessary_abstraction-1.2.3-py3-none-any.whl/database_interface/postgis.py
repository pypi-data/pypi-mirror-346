from typing import Literal
import atexit
from collections import ChainMap

from .postgresql import PostgreSQL
from .db_types import POSTGIS_TYPE_MAP
from .sql_objects import Select, Where, Update, Insert, Join, SpatialJoin, JOIN_TYPE
from .schema_objects import TableSchema, Column
from .errors import DatabaseError, Error


GEOM_TYPES = ("point", "linestring", "polygon", "multipoint", "multilinestring", "multipolygon", 
              "geometry collection", "pointz", "linestringz", "polygonz", "multipointz", 
              "multilinestringz", "multipolygonz", "pointm", "linestringm", "polygonm", "multipointm", 
              "multilinestringm", "multipolygonm", "pointzm", "linestringzm", "polygonzm", "multipointzm", 
              "multilinestringzm", "multipolygonzm", "point geography", "linestring geography", 
              "polygon geography", "multipoint geography", "multilinestring geography", 
              "multipolygon geography", "geometry collection geography")


def geom_statement(type:str, wkid:int):
    geom_map = {"point": f"geometry(Point, {wkid})", 
                "linestring": f"geometry(LineString, {wkid})", 
                "polygon": f"geometry(Polygon, {wkid})", 
                "multipoint": f"geometry(MultiPoint, {wkid})", 
                "multilinestring": f"geometry(MultiLineString, {wkid})", 
                "multipolygon": f"geometry(MultiPolygon, {wkid})", 
                "geometry collection": f"geometry(GeometryCollection, {wkid})", 
                "pointz": f"geometry(PointZ, {wkid})", 
                "linestringz": f"geometry(LineStringZ, {wkid})", 
                "polygonz": f"geometry(PolygonZ, {wkid})", 
                "multipointz": f"geometry(MultiPointZ, {wkid})", 
                "multilinestringz": f"geometry(MultiLineStringZ, {wkid})", 
                "multipolygonz": f"geometry(MultiPolygonZ, {wkid})", 
                "pointm": f"geometry(PointM, {wkid})", 
                "linestringm": f"geometry(LineStringM, {wkid})", 
                "polygonm": f"geometry(PolygonM, {wkid})", 
                "multipointm": f"geometry(MultiPointM, {wkid})", 
                "multilinestringm": f"geometry(MultiLineStringM, {wkid})", 
                "multipolygonm": f"geometry(MultiPolygonM, {wkid})", 
                "pointzm": f"geometry(PointZM, {wkid})", 
                "linestringzm": f"geometry(LinestringZM, {wkid})", 
                "polygonzm": f"geometry(PolygonZM, {wkid})", 
                "multipointzm": f"geometry(MultiPointZM, {wkid})", 
                "multilinestringzm": f"geometry(MultiLineStringZM, {wkid})", 
                "multipolygonzm": f"geometry(MultiPolygonZM, {wkid})", 
                "point geography": f"geography(Point)", 
                "linestring geography": f"geography(LineString)", 
                "polygon geography": f"geography(Polygon)", 
                "multipoint geography": f"geography(MultiPoint)", 
                "multilinestring geography": f"geography(MultiLineString)", 
                "multipolygon geography": f"geography(MultiPolygon)", 
                "geometry collection geography": "geography"}
    
    return geom_map[type]



class PostGIS(PostgreSQL):
    def __init__(self, db_name:str, username:str, password:str, schema:str, host:str="localhost", port:int=5432, geometry_extract:Literal["WKT", "WKB"]="WKT"):
        super().__init__(db_name, username, password, schema, host, port)
        self.__binding_char = "%s"
        self.__type_map = POSTGIS_TYPE_MAP
        self.__extract_mode = geometry_extract

        with self.cursor() as cur:
            cur.execute("SELECT extname FROM pg_extension WHERE extname = 'postgis';")
            if not cur.fetchall():
                raise DatabaseError(Error.INVALID_POSTGIS_CONNECTION)

        atexit.register(self.close)

    @property
    def type_map(self) -> dict:
        return self.__type_map

    def create_table_statement(self, table_name:str, schema:TableSchema) -> str:
        statement = f"CREATE TABLE IF NOT EXISTS {self.table(table_name)} ("
        for sql_col in schema.columns:
            if sql_col.data_type in GEOM_TYPES:
                statement += f"{sql_col.name} {geom_statement(sql_col.data_type, sql_col.spatial_ref)}"
            else:
                statement += f"{sql_col.name} {self.type_map[sql_col.data_type]}"
            if sql_col.primary_key:
                statement = statement + f" PRIMARY KEY"
            if sql_col.unique and not sql_col.primary_key:
                statement = statement + f" UNIQUE"
            if not sql_col.nullable and not sql_col.primary_key:
                statement = statement + f" NOT NULL"
            if sql_col.default:
                statement = statement + f" DEFAULT {sql_col.default}"
            if sql_col.check_constraint:
                statement = statement + f" {sql_col.check_constraint.query}"
            if sql_col.foreign_key:
                statement = statement + f" REFERENCES {self.table(sql_col.foreign_key.ref_table)} ({sql_col.foreign_key.ref_col})"
            statement = statement + ", "
        statement = statement[:-2] + f");"
        return statement
    
    def create_spatial_index(self, index_name:str, table_name:str, on_column:list[str]):
        with self.cursor() as cur:
            cur.execute(f"CREATE INDEX {index_name} ON {table_name} USING GIST({on_column})")

    def select(self, table_name:str, cols:list[str]=["*"], where:Where=None) -> list[tuple]:
        schema = self.get_schema(table_name, cols)

        if self.__extract_mode == "WKT":
            cols = list(schema.col_name_list)
            for i, d_type in enumerate(schema.data_type_list):
                if d_type == "geometry":
                    cols[i] = f"ST_AsText({cols[i]})"

        query, params = Select(cols).from_(self.table(table_name)).concat_where(where).build(self.__binding_char)
        with self.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
        
        return self.convert_types(schema, rows, "select")

    def spatial_join_contains(self, left_table:str, right_table:str, left_on:str, right_on:str, return_cols:list[str]=["*"], type:JOIN_TYPE="INNER", where:Where=None):
        left_schema = self.get_schema(left_table)
        right_schema = self.get_schema(right_table)

        dupe_col_names = left_schema.col_name_set.intersection(right_schema.col_name_set)
        if dupe_col_names.intersection(return_cols):
            raise DatabaseError(Error.AMBIGUOUS_COLUMN_NAMES)
        
        if self.__extract_mode == "WKT":
            for col in dupe_col_names:
                    left_schema.column_map[col].name = f"{left_table}.{col}"
                    right_schema.column_map[col].name = f"{right_table}.{col}"

            combined_map = ChainMap(left_schema.column_map, right_schema.column_map)
            if return_cols == ["*"]:
                schema = TableSchema(tuple(combined_map[col] for col in combined_map))
            else:
                schema = TableSchema(tuple(combined_map[col] for col in return_cols if col in combined_map))

            return_cols = list(schema.col_name_list)
            for i, d_type in enumerate(schema.data_type_list):
                if d_type == "geometry":
                    return_cols[i] = f"ST_AsText({return_cols[i]})"

        join = SpatialJoin(self.table(right_table), type).ST_Contains(left_on, right_on)
        query, params = Select(return_cols).from_(self.table(left_table)).join(join).concat_where(where).build(self.__binding_char)
        with self.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

        return rows
    
    def spatial_join_within(self, left_table:str, right_table:str, left_on:str, right_on:str, distance:float | int, return_cols:list[str]=["*"], type:JOIN_TYPE="INNER", where:Where=None):
        left_schema = self.get_schema(left_table)
        right_schema = self.get_schema(right_table)

        dupe_col_names = left_schema.col_name_set.intersection(right_schema.col_name_set)
        if dupe_col_names.intersection(return_cols):
            raise DatabaseError(Error.AMBIGUOUS_COLUMN_NAMES)
        
        if self.__extract_mode == "WKT":
            for col in dupe_col_names:
                    left_schema.column_map[col].name = f"{left_table}.{col}"
                    right_schema.column_map[col].name = f"{right_table}.{col}"

            combined_map = ChainMap(left_schema.column_map, right_schema.column_map)
            if return_cols == ["*"]:
                schema = TableSchema(tuple(combined_map[col] for col in combined_map))
            else:
                schema = TableSchema(tuple(combined_map[col] for col in return_cols if col in combined_map))

            return_cols = list(schema.col_name_list)
            for i, d_type in enumerate(schema.data_type_list):
                if d_type == "geometry":
                    return_cols[i] = f"ST_AsText({return_cols[i]})"

        join = SpatialJoin(self.table(right_table), type).ST_DWithin(left_on, right_on, distance)
        query, params = Select(return_cols).from_(self.table(left_table)).join(join).concat_where(where).build(self.__binding_char)
        with self.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

        return rows
    
    def spatial_join_intersects(self, left_table:str, right_table:str, left_on:str, right_on:str, return_cols:list[str]=["*"], type:JOIN_TYPE="INNER", where:Where=None):
        left_schema = self.get_schema(left_table)
        right_schema = self.get_schema(right_table)

        dupe_col_names = left_schema.col_name_set.intersection(right_schema.col_name_set)
        if dupe_col_names.intersection(return_cols):
            raise DatabaseError(Error.AMBIGUOUS_COLUMN_NAMES)
        
        if self.__extract_mode == "WKT":
            for col in dupe_col_names:
                    left_schema.column_map[col].name = f"{left_table}.{col}"
                    right_schema.column_map[col].name = f"{right_table}.{col}"

            combined_map = ChainMap(left_schema.column_map, right_schema.column_map)
            if return_cols == ["*"]:
                schema = TableSchema(tuple(combined_map[col] for col in combined_map))
            else:
                schema = TableSchema(tuple(combined_map[col] for col in return_cols if col in combined_map))

            return_cols = list(schema.col_name_list)
            for i, d_type in enumerate(schema.data_type_list):
                if d_type == "geometry":
                    return_cols[i] = f"ST_AsText({return_cols[i]})"

        join = SpatialJoin(self.table(right_table), type).ST_Intersects(left_on, right_on)
        query, params = Select(return_cols).from_(self.table(left_table)).join(join).concat_where(where).build(self.__binding_char)
        with self.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

        return rows