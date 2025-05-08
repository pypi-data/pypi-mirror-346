from enum import Enum



class PortType(Enum):
    """Enum for the type of port."""

    INPUT = "input"
    OUTPUT = "output"


class DataType(Enum):
    """Enum for the data type of the port."""
    
    INT = "int"
    FLOAT = "float"
    STR = "str"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"
    TUPLE = "tuple"
    SET = "set"
    BYTE = "bytes"
    COMPLEX = "complex"
    CALLABLE = "callable"
    # Add more data types as needed
    
    
    
    
if __name__ == "__main__":
    
    print(DataType.CALLABLE.value)