"""Facilities for generating error messages during type checking.
"""


def cant_infer_query_statement() -> str:
    return "Cannot infer statement value."


def any_type_args_warn() -> str:
    return "Can not infer type of query argument. Please specify type."


def unsupported_type(type_name: str) -> str:
    return f'Unsupported for mapping type "{type_name}"'


def database_error(msg: str) -> str:
    return f"Database error: {msg}"


def func_name(fullname: str) -> str:
    return fullname.split(".")[-1]
