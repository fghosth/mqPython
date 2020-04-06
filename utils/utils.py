# 变量类型
INT = "int"
STRING = "string"
FLOAT = "float"
LIST = "list"
TUPLE = "tuple"
DICT = "dict"
SET = "set"


# 判断变量类型的函数
def Typeof(variate):
    type = None
    if isinstance(variate, int):
        type = INT
    elif isinstance(variate, str):
        type = STRING
    elif isinstance(variate, float):
        type = FLOAT
    elif isinstance(variate, list):
        type = LIST
    elif isinstance(variate, tuple):
        type = TUPLE
    elif isinstance(variate, dict):
        type = DICT
    elif isinstance(variate, set):
        type = SET
    return type




