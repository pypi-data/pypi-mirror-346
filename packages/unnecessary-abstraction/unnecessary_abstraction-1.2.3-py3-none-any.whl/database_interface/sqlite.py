import sqlite3
from collections import ChainMap
import atexit

from .database import Database
from .db_types import SQLITE_TYPE_MAP
from .schema_objects import TableSchema, Column
from .sql_objects import Select, Where, Update, Insert, Join, JOIN_TYPE
from .errors import DatabaseError, Error



class SQLite(Database):
    def __init__(self, sqlite_path:str=":memory:", use_foreign_keys=False):
        self.__binding_char = "?"
        self.__type_map = SQLITE_TYPE_MAP
        self.__conn = sqlite3.Connection(sqlite_path)
        if use_foreign_keys:
            with self.cursor() as cur:
                cur.execute("PRAGMA foreign_keys = ON")

        atexit.register(self.close)

    def table(self, table_name:str) -> str:
        return table_name
    @property
    def connection(self) -> sqlite3.Connection:
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
            cur.execute("SELECT name FROM sqlite_master")
            return tuple(table[0] for table in cur.fetchall())
    
    def get_schema(self, table_name:str, cols:list=["*"], throw_error:bool=True) -> TableSchema | None:
        with self.cursor() as cur:
            res = cur.execute(f"PRAGMA table_info({self.table(table_name)})").fetchall()
        if not res:
            if throw_error:
                raise DatabaseError(Error.TABLE_DOESNT_EXIST, table_name)
            else:
                return None

        if cols == ["*"]:
            return TableSchema(tuple(Column.shallow(col[1], col[2], col[0] + 1) for col in res))
        else:
            return TableSchema(tuple(Column.shallow(col[1], col[2], col[0] + 1) for col in res if col[1] in cols))

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
        
    def upsert(self, table_name:str, cols:list[str], rows:list[tuple], conflcit_col:str) -> None:
        schema = self.get_schema(table_name, cols)
        rows = self.convert_types(schema, rows, "insert")
        query, params = Insert(self.table(table_name), cols).values(rows).update_on_conflict(conflcit_col).build(self.__binding_char)
        with self.cursor() as cur:
            cur.executemany(query, params)

    def join(self, left_table:str, right_table:str, left_on:str, right_on:str, return_cols:list[str]=["*"], type:JOIN_TYPE="INNER", where:Where=None):
        left_schema = self.get_schema(left_table)
        right_schema = self.get_schema(right_table)

        dupe_col_names = left_schema.col_name_set.intersection(right_schema.col_name_set)
        if dupe_col_names.intersection(return_cols):
            raise DatabaseError(Error.AMBIGUOUS_COLUMN_NAMES)
        
        for col in dupe_col_names:
                left_schema.column_map[col].name = f"{left_table}.{col}"
                right_schema.column_map[col].name = f"{right_table}.{col}"

        combined_map = ChainMap(left_schema.column_map, right_schema.column_map)
        if return_cols == ["*"]:
            schema = TableSchema(tuple(combined_map[col] for col in combined_map))
        else:
            schema = TableSchema(tuple(combined_map[col] for col in return_cols if col in combined_map))

        join = Join(self.table(right_table), type).on_columns(left_on, right_on)
        query, params = Select(return_cols).from_(self.table(left_table)).join(join).concat_where(where).build(self.__binding_char)
        with self.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
        rows = self.convert_types(schema, rows, "select")

        return rows
