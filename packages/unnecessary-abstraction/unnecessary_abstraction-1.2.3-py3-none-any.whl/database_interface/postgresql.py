from .database import Database
import psycopg2
import atexit
from collections import ChainMap

from .schema_objects import TableSchema, Column
from .sql_objects import Select, Where, Update, Insert, Join, JOIN_TYPE
from .db_types import POSTGRES_TYPE_MAP, POSTGRES_TYPES
from .errors import DatabaseError, Error

class PostgreSQL(Database):
    def __init__(self, db_name:str, username:str, password:str, namespace:str, host="localhost", port=5432):
        self.__conn = psycopg2.connect(database=db_name, user=username, password=password, host=host, port=port)
        self.__binding_char = "%s"
        self.__type_map = POSTGRES_TYPE_MAP
        self.__namespace = namespace

        atexit.register(self.close)

    def table(self, table_name:str) -> str:
        return f"{self.__namespace}.{table_name}"
    @property
    def namespace(self):
        return self.__namespace
    @property
    def connection(self) -> psycopg2.extensions.connection:
        return self.__conn
    @property
    def type_map(self) -> dict:
        return self.__type_map
    @property
    def binding_char(self) -> str:
        return self.__binding_char
    @property
    def table_list(self) -> tuple[str]:
        with self.cursor() as cur:
            cur.execute((f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.__namespace}'"))
            return tuple(table[0] for table in cur.fetchall())
    
    def get_schema(self, table_name:str, cols:list=["*"]) -> TableSchema | None:
        GET_COL_SCHEMA = f"""
        SELECT column_name, data_type, ordinal_position, udt_name
        FROM information_schema.columns 
        WHERE table_schema='{self.__namespace}' AND table_name='{table_name}'
        """
        with self.cursor() as cur:
            cur.execute(GET_COL_SCHEMA)
            res = cur.fetchall()
        if not res:
            return None
        
        schema = []
        if cols == ["*"]:
            for col in res:
                if col[1] == "USER-DEFINED":
                    schema.append(Column.shallow(col[0], col[3], col[2]))
                else:
                    schema.append(Column.shallow(col[0], col[1], col[2]))
        else:
            for col in res:
                if col[0] in cols:
                    if col[1] == "USER-DEFINED":
                        schema.append(Column.shallow(col[0], col[3], col[2]))
                    else:
                        schema.append(Column.shallow(col[0], col[1], col[2]))
        
        return TableSchema(schema)

    def select(self, table_name:str, cols:list[str]=["*"], where:Where=None) -> list[tuple]:
        query, params = Select(cols).from_(self.table(table_name)).concat_where(where).build(self.__binding_char)
        with self.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
        
        schema = self.get_schema(table_name, cols)
        return self.convert_types(schema, rows, "select")

    def insert(self, table_name:str, cols:list[str], rows:list[tuple]) -> None:
        schema = self.get_schema(table_name, cols)
        rows = self.convert_types(schema, rows, "insert")
        query, params = Insert(self.table(table_name), cols).values(rows).build(self.__binding_char)

        with self.cursor() as cur:
            cur.executemany(query, params)

    def update(self, table_name:str, cols:list[str], rows:list[tuple], where:Where) -> None:
        if where.id_index != None:
            rows = [row + (row[where.id_index],) for row in rows]
        elif where.id_list:
            rows = [row + (id,) for row, id in zip(rows, where.id_list)]

        schema = self.get_schema(table_name, cols)
        rows = self.convert_types(schema, rows, "insert")
        query, params = Update(self.table(table_name)).set(cols).to_values(rows).concat_where(where).build(self.__binding_char)
        with self.cursor() as cur:
            cur.executemany(query, params)

    def upsert(self, table_name:str, cols:list[str], rows:list[tuple], conflict_col:str) -> None:
        schema = self.get_schema(table_name, cols)
        rows = self.convert_types(schema, rows, "insert")
        query, params = Insert(self.table(table_name), cols).values(rows).update_on_conflict(conflict_col).build(self.__binding_char)
        with self.cursor() as cur:
            cur.executemany(query, params)

    def join(self, left_table:str, right_table:str, left_on:str, right_on:str, return_cols:list[str]=["*"], type:JOIN_TYPE="INNER", where:Where=None):
        left_schema = self.get_schema(left_table)
        right_schema = self.get_schema(right_table)

        dupe_col_names = left_schema.col_name_set.intersection(right_schema.col_name_set)
        if dupe_col_names.intersection(return_cols):
            raise DatabaseError(Error.AMBIGUOUS_COLUMN_NAMES)

        join = Join(self.table(right_table), type).on_columns(left_on, right_on)
        query, params = Select(return_cols).from_(self.table(left_table)).join(join).concat_where(where).build(self.__binding_char)
        with self.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

        return rows