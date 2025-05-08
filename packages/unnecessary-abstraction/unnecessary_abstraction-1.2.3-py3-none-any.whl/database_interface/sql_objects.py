from typing import Literal
from .errors import DatabaseError, Error

AGGREGATE_FUNCS = Literal["Count", "Sum", "Average", "Max", "Min", "Median", "Variance", "Standard Deviation"]
DATABASE_TYPE = Literal["SQLite", "PostgreSQL"]
JOIN_TYPE = Literal["INNER", "RIGHT", "LEFT", "OUTER"]

class SQL:
    __slots__ = ("query", "params")
    def __init__(self):
        self.query:str = ""
        self.params:list = []
    
    def build(self, token:Literal["?", "%s"]):
        return self.query.replace("?", token), tuple(self.params)

class LogicOperators(SQL):
    def and_(self, column):
        self.query += f" AND {column}"
        return self
    
    def or_(self, column):
        self.query += f" OR {column}"
        return self
    
    def not_(self, column):
        self.query += f" NOT {column}"
        return self
    
    def is_null(self, column):
        self.query += f" {column} IS NULL"
        return self

    def not_null(self, column):
        self.query += f" {column} IS NOT NULL"
        return self
    
    def between(self, value1, value2):
        self.query += f" BETWEEN ? AND ?"
        self.params.append(value1)
        self.params.append(value2)
        return self
    
    def is_(self, operator:Literal[">", "<", ">=", "<=", "=", "!="], value):
        match operator:
            case "<":
                self.query += f" < ?"
            case ">":
                self.query += f" > ?"
            case "<=":
                self.query += f" <= ?"
            case ">=":
                self.query += f" >= ?"
            case "=":
                self.query += f" = ?"
            case "!=":
                self.query += f" != ?"
        self.params.append(value)
        return self

    def in_(self, values:list | tuple):
        placeholders = ', '.join('?' for _ in values)
        self.query += f" IN ({placeholders})"
        self.params.extend(values)
        return self

    def not_in(self, values:list | tuple):
        placeholders = ', '.join('?' for _ in values)
        self.query += f" NOT IN ({placeholders})"
        self.params += values
        return self

    def like(self, value:str):
        self.query += f" LIKE ?"
        self.params.append(value)
        return self

    def not_like(self, value:str):
        self.query += f" NOT LIKE ?"
        self.params.append(value)
        return self


class Having(LogicOperators):
    def __init__(self, column, function:AGGREGATE_FUNCS):
        super().__init__()
        match function:
            case "Count":
                self.query = f"HAVING COUNT({column})"
            case "Average":
                self.query = f"HAVING AVG({column})"
            case "Sum":
                self.query = f"HAVING SUM({column})"
            case "Max":
                self.query = f"HAVING MAX({column})"
            case "Min":
                self.query = f"HAVING MIN({column})"
            case "Median":
                self.query = f"HAVING MEDIAN({column})"
            case "Variance":
                self.query = f"HAVING VARIANCE({column})"
            case "Standard Deviation":
                self.query = f"HAVING STDDEV({column})"

class DQL(SQL):
    def from_(self, table):
        self.query += f" FROM {table}"
        return self
    
    def where(self, column):
        self.query += f" WHERE {column}"
        return self

    def group_by(self, column, having_clause:Having=None):
        self.query += f" GROUP BY {column}"
        return self
    
    def order_by(self, column, ordering:Literal["descending", "ascending"]="ascending"):
        match ordering:
            case "ascending":
                self.query += f" ORDER BY {column}"
            case "descending":
                self.query += f" ORDER BY {column} DESC"
        return self
    
    def limit(self, amount):
        self.query += f" LIMIT {amount}"
        return self
    
    def as_(self, alias):
        self.query += f" AS {alias}"
        return self


class Where(LogicOperators):
    def __init__(self, column):
        super().__init__()
        self.query += f"WHERE {column}"
        self.id_list = None
        self.id_index = None
    
    def equal_to_ids(self, id_list:list | tuple[str | int]):
        self.id_list = id_list
        self.query += " = ?"
        self.id_index = None
        return self
    def equal_to_index_pos(self, id_index:int):
        self.id_index = id_index
        self.query += " = ?"
        self.id_list = None
        return self


class Join(SQL):
    def __init__(self, right_table:str, type:JOIN_TYPE):
        super().__init__()
        self.query += f"{type} JOIN {right_table} "
        self.right_table = right_table

    def on_columns(self, left_on, right_on):
        self.query += f"ON {left_on} = {right_on}"
        return self

class SpatialJoin(SQL):
    def __init__(self, right_table:str, type:JOIN_TYPE):
        super().__init__()
        self.query += f"{type} JOIN {right_table} "
        self.right_table = right_table

    def ST_Contains(self, left_on, right_on):
        self.query += f"ON ST_Contains({right_on}, {left_on})"
        return self
    
    def ST_DWithin(self, left_on, right_on, distance):
        self.query += f"ON ST_DWithin({right_on}, {left_on}, {distance})"
        return self
    
    def ST_Intersects(self, left_on, right_on):
        self.query += f"ON ST_Intersects({right_on}, {left_on})"
        return self

class Select(LogicOperators, DQL):
    def __init__(self, columns:list[str]=["*"]):
        super().__init__()
        self.query += f"SELECT " + ", ".join(columns)
    
    def concat_where(self, where:Where | None):
        if where:
            self.query += " " + where.query
            self.params += where.params
        return self
    
    def join(self, join:Join):
        self.query += " " + join.query
        return self
    def spatial_join(self, join:SpatialJoin):
        pass


class Insert(LogicOperators, DQL):
    def __init__(self, table:str, columns:list | tuple[str]):
        super().__init__()
        self.__insert_columns = columns
        self.query = f"INSERT INTO {table} (" + ", ".join(columns) + ")"

    def values(self, to_values:list[list | tuple]):
        if not isinstance(to_values[0], (list, tuple)):
            raise DatabaseError(Error.INVALID_ROW_INPUT)
        
        self.query += f" VALUES ("
        for _ in range(len(to_values[0])):
            self.query += "?, "

        self.query = self.query[:-2] + ")"
        self.params += to_values

        return self
    
    def select(self, columns):
        self.query += f" SELECT {columns}"
        return self

    def update_on_conflict(self, conflict_col:str):
        self.query += f" ON CONFLICT ({conflict_col}) DO UPDATE SET "
        for col in self.__insert_columns:
            if col != conflict_col:
                self.query += f"{col} = EXCLUDED.{col}, "
        self.query = self.query[:-2]
        return self

class Update(LogicOperators, DQL):
    def __init__(self, table):
        super().__init__()
        self.query = f"UPDATE {table} "
    
    def set(self, columns:list[str]):
        self.query += f"SET " + " = ?, ".join(columns) + " = ?"
        return self
    
    def to_values(self, to_values:list | tuple):
        self.params += to_values
        return self

    def concat_where(self, where:Where | None):
        if where:
            self.query += " " + where.query
            self.params += where.params
        return self
    
    def from_subquery(self, subquery:Select):
        pass







class Check:
    def __init__(self, column):
        self.query = f"CHECK ({column} "
    
    def build(self):
        return self.query + ")"

    def and_(self, column):
        self.query += f" AND {column}"
        return self
    
    def or_(self, column):
        self.query += f" OR {column}"
        return self
    
    def not_(self, column):
        self.query += f" NOT {column}"
        return self
    
    def is_null(self, column):
        self.query += f" {column} IS NULL"
        return self

    def not_null(self, column):
        self.query += f" {column} IS NOT NULL"
        return self
    
    def between(self, value1, value2):
        self.query += f" BETWEEN {value1} AND {value2}"
        return self
    
    def is_(self, operator:Literal[">", "<", ">=", "<=", "=", "!="], value):
        match operator:
            case "<":
                self.query += f" < {value}"
            case ">":
                self.query += f" > {value}"
            case "<=":
                self.query += f" <= {value}"
            case ">=":
                self.query += f" >= {value}"
            case "=":
                self.query += f" = {value}"
            case "!=":
                self.query += f" != {value}"
        return self

    def in_(self, values:list | tuple):
        self.query += f" IN ({values})"
        return self

    def not_in(self, values:list | tuple):
        self.query += f" NOT IN ({values})"
        return self

    def like(self, value:str):
        self.query += f" LIKE {value}"
        return self

    def not_like(self, value:str):
        self.query += f" NOT LIKE {value}"
        return self

