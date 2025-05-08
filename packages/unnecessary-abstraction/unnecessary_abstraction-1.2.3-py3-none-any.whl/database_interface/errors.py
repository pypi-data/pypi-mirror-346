from enum import IntEnum

class Error(IntEnum):
    INVALID_POSTGIS_CONNECTION = 1
    EMPTY_RECORDS_INPUT = 2
    AMBIGUOUS_COLUMN_NAMES = 3
    TABLE_DOESNT_EXIST = 4
    NOT_JSONABLE_PYOBJECT = 5
    MIXED_COLUMN_DATATYPES = 6
    INVALID_RECORD_FORMAT_UNK_LIST = 7
    INVALID_RECORD_FORMAT_UNK_DICT = 8
    INVALID_ROW_INPUT = 9

AMBIGUOUS_COLUMN_NAMES_MESSAGE = """
There are duplicate column names between the two tables you are joining.
Indicate these column names as table_name.column_name in the return_cols 
arguement.
"""

NOT_JSONABLE_PYOBJECT_MESSAGE = """
Your data contains a python dictionary that cannot be formed into a JSON.
Check the values of your dictionary to find what is causing json.dumps()
to error out and convert as necessary. PostgreSQL doesn't have any type
to support this data structure.
"""

INVALID_ROW_INPUT_MESSAGE = """
The rows of data you attempted to pass need to be a list or tuple containing
list or tuples that represent each row. Even single row inserts need to be
wrapped into an additional list or tuple.
"""


class DatabaseError(Exception):
    def __init__(self, error:Error, table_name:str="", col_name:str=""):
        message = ""
        match error:
            case Error.INVALID_POSTGIS_CONNECTION:
                message = "The PostgreSQL you connected to does not have the PostGIS extension enabled."
            case Error.AMBIGUOUS_COLUMN_NAMES:
                message = AMBIGUOUS_COLUMN_NAMES_MESSAGE
            case Error.TABLE_DOESNT_EXIST:
                message = f"{table_name} doesn't exist in database."
            case Error.EMPTY_RECORDS_INPUT:
                message = "Records passed to records_to_table() are empty"
            case Error.NOT_JSONABLE_PYOBJECT:
                message = NOT_JSONABLE_PYOBJECT_MESSAGE
            case Error.MIXED_COLUMN_DATATYPES:
                message = f"{col_name} contains different datatypes in it's column."
            case Error.INVALID_RECORD_FORMAT_UNK_LIST:
                message:str = "Within your list of table records contains a data structure that isn't a valid dictionary"
            case Error.INVALID_RECORD_FORMAT_UNK_DICT:
                message:str = "Within your dictionary of table columns contains a data structure that isn't a valid list of row values"
            case Error.INVALID_ROW_INPUT:
                message:str = INVALID_ROW_INPUT_MESSAGE
                
        super().__init__(message)


