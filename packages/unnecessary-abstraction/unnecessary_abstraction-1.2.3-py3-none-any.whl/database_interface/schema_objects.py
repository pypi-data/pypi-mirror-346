from typing import NamedTuple
from .db_types import POSTGIS_TYPES, POSTGRES_TYPES, SQLITE_TYPES
from .sql_objects import Check

class ForeignKey(NamedTuple):
    ref_table:str
    ref_col:str

class Column:
    __slots__ = ('name', 'data_type', 'position', 'nullable', 'primary_key', 'foreign_key', 'unique', 'default', 'check_constraint', 'spatial_ref', '__shallow_schema')
    def __init__(self, name:str, data_type:SQLITE_TYPES | POSTGRES_TYPES | POSTGIS_TYPES, 
                 position:int=1, primary_key:bool=False, foreign_key:ForeignKey=None, 
                 nullable=True, unique:bool=False, default=None, check_constraint:Check=None, 
                 spatial_ref:int=4326):

        self.name:str = name
        self.data_type:SQLITE_TYPES | POSTGRES_TYPES | POSTGIS_TYPES = data_type
        self.position:int = position

        self.primary_key:bool = primary_key
        self.foreign_key:ForeignKey = foreign_key
        self.nullable:bool = nullable
        self.unique:bool = unique
        self.default = default
        self.check_constraint:Check = check_constraint
        self.spatial_ref:int = spatial_ref

        self.__shallow_schema:bool = False

    @classmethod
    def shallow(cls, name:str, data_type:SQLITE_TYPES | POSTGRES_TYPES | POSTGIS_TYPES, position:int):
        col = cls(name, data_type, position)
        col.__shallow_schema = True
        del col.primary_key, col.foreign_key, col.nullable, col.unique, col.default, col.check_constraint, col.spatial_ref
        return col

    def __repr__(self) -> str:
        return str(self.to_dict)
    
    @property
    def to_dict(self) -> dict:
        if self.__shallow_schema:
            return {"name": self.name, "data_type": self.data_type, "position": self.position}
        else:
            return {"name": self.name, "data_type": self.data_type, "position": self.position, "primary_key": self.primary_key,
                    "foreign_key": self.foreign_key, "nullable": self.nullable, "unique": self.unique, "default": self.default,
                    "check_constraint": self.check_constraint, "spatial_ref": self.spatial_ref}

class TableSchema:
    __slots__ = ('__columns')
    def __init__(self, columns:list | tuple[Column]):
        self.__columns:tuple[Column] = tuple(col for col in columns)
        self.order_columns()

    @property
    def columns(self) -> tuple[Column]:
        return self.__columns
    @property
    def column_map(self) -> dict[str, Column]:
        return {col.name: col for col in self.__columns}
    @property
    def col_name_set(self) -> set[str]:
        return set(col.name for col in self.__columns)
    @property
    def col_name_list(self) -> tuple[str]:
        return tuple(col.name for col in self.__columns)
    @property
    def data_type_list(self) -> tuple[str]:
        return tuple(col.data_type for col in self.__columns)
    @property
    def positions_list(self) -> tuple[int]:
        return tuple(col.position for col in self.__columns)

    def order_columns(self) -> None:
        pos_list = sorted(self.positions_list)
        if pos_list == tuple(range(min(pos_list), max(pos_list)+1)) and pos_list[0] == 1:
            self.order_by_position_id()
        else:
            self.order_by_location()

    def order_by_location(self) -> None:
        for pos, column in enumerate(self.__columns):
            column.position = pos + 1

    def order_by_position_id(self) -> None:
        self.__columns = tuple(sorted(self.__columns, key=lambda x: x.position))

    def filter_columns(self, col_name_list:list) -> None:
        self.__columns = tuple(col for col in self.__columns if col in col_name_list)
        self.order_by_location()
    
    def __repr__(self) -> str:
        text = ""
        for i in self.to_dict:
            text += str(i) + "\n"
        return text

    @property
    def to_dict(self) -> tuple[dict]:
        return tuple(col.to_dict for col in self.__columns)