import csv, json, pathlib, sqlite3, copy
from datetime import datetime
from typing import Protocol, Literal
from uuid import UUID
from decimal import Decimal
from contextlib import contextmanager
from collections import defaultdict
import psycopg2
import psycopg2._psycopg

from .schema_objects import Column, TableSchema
from .db_types import POSTGIS_TYPES, POSTGRES_TYPES, SQLITE_TYPES
from .sql_objects import Select, Where, Update, Insert, JOIN_TYPE
from .errors import DatabaseError, Error

class Database(Protocol):
    def close(self) -> None:
        self.connection.close()
    @contextmanager
    def cursor(self):
        cur = self.connection.cursor()
        try:
            yield cur
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cur.close()
    
    def table(self, table_name:str) -> str:
        ...
    def get_schema(self, table_name:str, cols:list=["*"]) -> TableSchema | None:
        ...
    @property
    def connection(self) -> psycopg2.extensions.connection | sqlite3.Connection:
        ...
    @property
    def type_map(self) -> dict:
        ...
    @property
    def binding_char(self) -> str:
        ...
    @property
    def table_list(self):
        ...

    def select(self, table_name:str, cols:list[str]=["*"], where:Where=None) -> list[tuple]:
        ...
    def insert(self, table_name:str, cols:list[str], rows:list[tuple]) -> None:
        ...
    def update(self, table_name:str, cols:list[str], rows:list[tuple], where:Where) -> None:
        ...
    def upsert(self, table_name:str, cols:list[str], rows:list[tuple], id_col_name:str) -> None:
        ...
    def join(self, left_table:str, right_table:str, left_on:str, right_on:str, return_cols:list[str]=["*"], type:JOIN_TYPE="INNER", where:Where=None):
        ...
    def delete(self, table_name:str, where:Where) -> None:
        query = f"DELETE FROM {self.table(table_name)}"
        params = ()
        if where:
            w_query, w_params = where.build(self.binding_char)
            query += " " + w_query
            params = w_params
        query += ";"
        with self.cursor() as cur:
            cur.execute(query, params)


    def insert_records_to_table(self, table_name:str, table_records:list[dict]) -> None:
        if table_records:
            cols = list(table_records[0].keys())
        else:
            raise DatabaseError(Error.EMPTY_RECORDS_INPUT)

        table_rows = tuple(tuple(val for val in row.values()) for row in table_records)
        self.insert(table_name, cols, table_rows)

    def update_records_to_table(self, table_name:str, table_records:list[dict], where:Where) -> None:
        if table_records:
            cols = list(table_records[0].keys())
        else:
            raise DatabaseError(Error.EMPTY_RECORDS_INPUT)
        
        table_rows = tuple(tuple(val for val in row.values()) for row in table_records)
        self.update(table_name, cols, table_rows, where)
    
    def upsert_records_to_table(self, table_name:str, table_records:list[dict], id_col_name:str) -> None:
        if table_records:
            cols = list(table_records[0].keys())
        else:
            raise DatabaseError(Error.EMPTY_RECORDS_INPUT)
        
        table_rows = tuple(tuple(val for val in row.values()) for row in table_records)
        self.upsert(table_name, cols, table_rows, id_col_name)

    def table_to_records(self, table_name:str, cols:list[str]=["*"], where:Where=None) -> list[dict]:
        schema = self.get_schema(table_name, cols)
        if not schema:
            raise DatabaseError(Error.TABLE_DOESNT_EXIST, table_name=self.table(table_name))
        
        table_data = self.select(table_name, cols, where)

        records = []
        for row in table_data:
            records.append({col.name: row[col.position - 1] for col in schema.columns})

        return records

    ### TABLE ALTERATIONS ###

    def delete_all_records(self, table_name:str) -> None:
        with self.cursor() as cur:
            cur.execute(f"DELETE FROM {self.table(table_name)};")

    def add_column(self, table_name:str, col_name:str, data_type:SQLITE_TYPES | POSTGRES_TYPES | POSTGIS_TYPES) -> None:
        with self.cursor() as cur:
            cur.execute(f"ALTER TABLE {self.table(table_name)} ADD {col_name} {self.type_map[data_type]};")
    
    def drop_column(self, table_name:str, col_name:str) -> None:
        with self.cursor() as cur:
            cur.execute(f"ALTER TABLE {self.table(table_name)} DROP COLUMN {col_name}")
    
    def rename_column(self, table_name:str, col_name:str, new_col_name:str) -> None:
        with self.cursor() as cur:
            cur.execute(f"ALTER TABLE {self.table(table_name)} RENAME COLUMN {col_name} TO {new_col_name}")

    def rename_table(self, table_name:str, new_table_name:str) -> None:
        with self.cursor() as cur:
            cur.execute(f"ALTER TABLE {self.table(table_name)} RENAME TO {new_table_name}")
        
    ### TABLE ALTERATIONS ###
    
    ### TABLE CREATION ###
    def create_table_from_records(self, table_name:str, table_records:list[dict], col_overrides:list[Column]=[]) -> None:
        schema = self.evaluate_schema(table_records, col_overrides)
        self.create_blank_table(table_name, schema)
        self.insert_records_to_table(table_name, table_records)

    def create_blank_table(self, table_name:str, schema:TableSchema) -> None:
        sql = self.create_table_statement(table_name, schema)
        with self.cursor() as cur:
            cur.execute(sql)
    
    def create_table_statement(self, table_name:str, schema:TableSchema) -> str:
        statement = f"CREATE TABLE IF NOT EXISTS {self.table(table_name)} ("
        for sql_col in schema.columns:
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
                statement = statement + f" {sql_col.check_constraint.build()}"
            if sql_col.foreign_key:
                statement = statement + f" REFERENCES {self.table(sql_col.foreign_key.ref_table)} ({sql_col.foreign_key.ref_col})"
            statement = statement + ", "
        statement = statement[:-2] + f");"
        return statement

    def create_index(self, index_name:str, table_name:str, on_column:str, unique:bool=False) -> None:
        with self.cursor() as cur:
            if unique:
                cur.execute(f"CREATE UNIQUE INDEX {index_name} ON {table_name} ({on_column})")
            else:
                cur.execute(f"CREATE INDEX {index_name} ON {table_name} ({on_column})")

    def create_composite_index(self, index_name:str, table_name:str, on_columns:list[str]):
        on_columns = ", ".join(on_columns)
        with self.cursor() as cur:
            cur.execute(f"CREATE INDEX {index_name} ON {table_name} ({on_columns})")

    def create_partial_index(self, index_name:str, table_name:str, on_column:str, where:Where):
        with self.cursor() as cur:
            cur.execute(f"CREATE INDEX {index_name} ON {table_name} ({on_column}) {where.query}")

    ### TABLE CREATION ###

    #### CSV Functions #####

    @staticmethod
    def rename_duplicate_columns(fieldname_list:list[str]) -> list[str]:
        d = defaultdict(list)
        [d[name].append(seq) for seq, name in enumerate(fieldname_list)]
        for col, count in d.items():
            if len(count) > 1:
                for seq, index in enumerate(count[1:]):
                    fieldname_list[index] = f"{fieldname_list[index]}_{seq+2}"
        return fieldname_list
    
    @staticmethod
    def csv_to_records(csv_path:str) -> list[dict]:
        csv_path:pathlib.Path = pathlib.Path(csv_path)
        with open(csv_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            if len(reader.fieldnames) != len(set(reader.fieldnames)):
                reader.fieldnames = Database.rename_duplicate_columns(reader.fieldnames)
            records = [row for row in reader]
        
        for row in records:
            for key, val in row.items():
                if val == '':
                    row[key] = None
        return records
    
    @staticmethod
    def records_to_csv(csv_name:str, table_records:list[dict], csv_path:str=".") -> None:
        headers = table_records[0].keys()
        with open(f"{csv_path}\\{csv_name}.csv", "w", newline='') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(table_records)

    @staticmethod
    def csv_to_json(csv_path:str, json_save_path:str=".") -> None:
        table_name = pathlib.Path(csv_path).stem
        records = Database.csv_to_records(csv_path)
        Database.records_to_json(table_name, records, json_save_path)

    def csv_to_table(self, csv_path:str, table_name:str) -> None:
        records = Database.csv_to_records(csv_path)
        self.insert_records_to_table(table_name, records)

    def create_table_from_csv(self, csv_path:str) -> None:
        pass
    
    def schema_to_csv(self, table_name:str, save_path:str="."):
        schema = self.get_schema(table_name).to_dict
        Database.records_to_csv(f"{table_name}_schema", schema, save_path)

    def table_to_csv(self, table_name:str, file_name:str="", save_path:str=".", columns:str=["*"], where:Where=None) -> None:
        table_records = self.table_to_records(table_name, columns, where)
        if not file_name:
            file_name = table_name
        Database.records_to_csv(file_name, table_records, save_path)
    
    ### CSV Functions #####

    ### JSON Functions ####

    @staticmethod
    def json_to_records(json_path:str) -> list[dict]:
        json_path:pathlib.Path = pathlib.Path(json_path)
        with open(json_path, "r") as f:
            data = json.load(f)
        
        if type(data) == list or type(data) == tuple:
            invalid = tuple(False for row in data if type(row) != dict)
            if invalid:
                raise DatabaseError(Error.INVALID_RECORD_FORMAT_UNK_LIST)
        elif type(data) == dict:
            invalid = tuple(False for col in data.values() if not type(col) == list or type(col) == tuple)
            if invalid:
                raise DatabaseError(Error.INVALID_RECORD_FORMAT_UNK_DICT)
            data = Database.columnar_to_rows(data)
            
        return data

    @staticmethod
    def records_to_json(json_name:str, table_records:list[dict], json_path:str=".") -> None:
        with open(f"{json_path}\\{json_name}.json", "w") as f:
            json.dump(table_records, f, indent=2)

    @staticmethod
    def json_to_csv(json_path:str, csv_save_path:str=".") -> None:
        table_name = pathlib.Path(json_path).stem
        records = Database.json_to_records(json_path)
        Database.records_to_csv(table_name, records, csv_save_path)

    def json_to_table(self, json_path:str, table_name:str) -> None:
        records = self.json_to_records(json_path)
        self.insert_records_to_table(table_name, records)
    
    def create_table_from_json(self, json_path:str) -> None:
        pass

    def schema_to_json(self, table_name:str, save_path:str=".") -> None:
        schema = self.get_schema(table_name).to_dict
        self.records_to_json(f"{table_name}_schema", schema, save_path)

    def table_to_json(self, table_name:str, file_name:str="", save_path:str=".", columns:str=["*"], where:Where=None) -> None:
        table_data = self.table_to_records(table_name, columns, where)
        schema = self.get_schema(table_name, columns)

        datetime_cols = []
        for pos, d_type in enumerate(schema.data_type_list):
            if d_type in ("datetime", "timestamp with time zone", "timestamp without time zone", "timestamp"):
                datetime_cols.append(schema.col_name_list[pos])

        if datetime_cols:
            for row in table_data:
                for col in datetime_cols:
                    row[col] = row[col].isoformat()
        
        if not file_name:
            file_name = table_name
        Database.records_to_json(file_name, table_data, save_path)
    
    ### JSON Functions ####



    @staticmethod
    def rows_to_columnar(records:list | tuple[dict], return_tuples:bool=False) -> dict[list | tuple]:
        if return_tuples:
            return {col: tuple(row[col] for row in records) for col in records[0]}
        else:
            return {col: [row[col] for row in records] for col in records[0]}
    
    @staticmethod
    def columnar_to_rows(records:dict[list | tuple], return_tuples:bool=False) -> list | tuple[dict]:
        if return_tuples:
            return tuple(dict(zip(records.keys(), row)) for row in zip(*records.values()))
        else:
            return [dict(zip(records.keys(), row)) for row in zip(*records.values())]

    def evaluate_schema(self, records:list[dict] | dict[list], col_overrides:list[Column]=[]) -> TableSchema:
        if isinstance(records, (list, tuple)):
            records:dict[list] = Database.rows_to_columnar(records, True)

        schema = []
        overide_col_list = tuple(col.name for col in col_overrides)
        
        for pos, (col_name, col_data) in enumerate(records.items(), 1):
            if col_name in overide_col_list:
                col:Column = col_overrides[overide_col_list.index(col_name)]
                schema.append(Column(name=col.name, 
                                     data_type=self.type_map[col.data_type], 
                                     position=pos, 
                                     is_primary_key=col.primary_key, 
                                     foreign_key=col.foreign_key, 
                                     is_unique=col.unique, 
                                     check_constraint=col.check_constraint, 
                                     not_null=col.nullable, 
                                     default=col.default))
            else:
                col_type = tuple(self.infer_type(x)for x in col_data if x != None)
                if len(set(col_type)) > 1:
                    raise DatabaseError(Error.MIXED_COLUMN_DATATYPES, col_name=col_name)
                schema.append(Column(name=col_name, data_type=self.type_map[col_type[0]], position=pos))

        return TableSchema(schema)

    def convert_types(self, schema:TableSchema, rows:list[dict], op:Literal["insert", "select"]) -> list[dict]:
        def convert_numeric(numeric:float | Decimal, op:Literal["insert", "select"]) -> float:
            match op:
                case "insert":
                    if type(numeric) == Decimal:
                        return numeric.__float__()
                    else:
                        return numeric
                case "select":
                    if type(numeric) == Decimal:
                        return numeric.__float__()
                    else:
                        return numeric

        def convert_date(date_time:str | datetime, op:Literal["insert", "select"]) -> str | datetime:
            match op:
                case "insert":
                    if type(date_time) == datetime:
                        return date_time.isoformat()
                    else:
                        return date_time
                case "select":
                    if type(date_time) == str:
                        return datetime.fromisoformat(date_time)
                    else:
                        return date_time
            
        def convert_json(json_val:dict | list | tuple | str, op:Literal["insert", "select"]) -> str | dict | list | tuple:
            match op:
                case "insert":
                    if isinstance(json_val, (dict, list, tuple)):
                        return json.dumps(json_val)
                    else:
                        return json_val
                case "select":
                    if type(json_val) == str:
                        return json.loads(json_val)
                    else:
                        return json_val
            
        func_map = {
            "datetime": convert_date, 
            "json": convert_json, 
            "numeric": convert_numeric
        }
        
        mod_map = {pos: d_type for pos, d_type in enumerate(schema.data_type_list) if d_type in ("datetime", "json", "numeric")}
        if mod_map:
            return [tuple(func_map[mod_map[i]](val, op) if i in mod_map else val for i, val in enumerate(row))for row in rows]
        else:
            return rows
        
    def infer_type(self, val) -> str:
        def is_datetime(x) -> bool:
            try:
                datetime.fromisoformat(x)
                return True
            except ValueError:
                return False
            
        def string_jsonable(x) -> bool:
            try:
                json.loads(x)
                return True
            except (TypeError, OverflowError, json.decoder.JSONDecodeError):
                return False
        def dict_jsonable(x) -> bool:
            try:
                json.dumps(x)
                return True
            except (TypeError, OverflowError, json.decoder.JSONDecodeError):
                return False

        if type(val) == int:
            return "integer"
        elif type(val) == float:
            return "decimal"
        elif type(val) == bool:
            return "text"
        elif type(val) == UUID:
            return "uuid"
        elif type(val) == datetime:
            if val.tzinfo:
                return "timestamp with time zone"
            else:
                return "timestamp"
        elif type(val) == str:
            val:str
            split = val.split(".")
            if len(split) == 2 and split[0].isdigit() and split[1].isdigit():
                return "numeric"
            elif val.isdigit():
                return "numeric"
            elif is_datetime(val):
                if datetime.fromisoformat(val).tzinfo:
                    return "timestamp with time zone"
                else:
                    return "timestamp"
            elif string_jsonable(val):
                return "json"
            else:
                return "text"
        elif isinstance(val, (dict, list, tuple)):
            if dict_jsonable(val):
                return "json"
            else:
                raise DatabaseError(Error.NOT_JSONABLE_PYOBJECT)