from typing import Optional, Type

from errors import SsqlTypeError
from messages import any_type_args_warn
from mypy.typeops import try_getting_str_literals_from_type
from mypy.types import AnyType, get_proper_type


def get_literal_str(typ: Type) -> Optional[list[str]]:
    res = try_getting_str_literals_from_type(typ)
    return res


def get_statement(st) -> Optional[str]:
    statement: Optional[list[str]] = get_literal_str(st)
    if statement is None or len(statement) == 0:
        return None
    # TODO use all list if need
    return statement[0]


def get_arg_type(arg_type):
    # TODO check None argument (it's may be a valid value)
    proper_type = get_proper_type(arg_type)
    if isinstance(proper_type, AnyType):
        raise SsqlTypeError(any_type_args_warn())
    return proper_type
