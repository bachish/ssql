def query_generator() -> str:
    return "select * from table1"


def execute(query_statement: str, *args) -> str:
    return query_statement


def unknownRet():
    return "42"


def get_int() -> int:
    return 42


def get_str() -> str:
    return "forty-two"


def get_bool() -> bool:
    return True
