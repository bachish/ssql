"""Facilities for generating error messages during type checking.
"""


def cant_infer_query_statement(name: str) -> str:
    return f'Cannot infer statement value to "{func_name(name)}".'


def any_type_args(pos: int, name: str) -> str:
    return (
        f'Can not infer type of query argument {pos} to "{func_name(name)}". '
        + " Please specify type."
    )


def database_error(name: str, msg: str) -> str:
    return f"Database error in {func_name(name)}: {msg}"


def func_name(fullname: str) -> str:
    return fullname.split(".")[-1]
