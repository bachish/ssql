import builtins
from typing import Optional

from ssql.core.mapper import Mapper


def get_statement(statement_type) -> Optional[str]:
    """check that query has string type and get it's value"""
    arg_type = Mapper.typeFromLiterals(statement_type)
    if not isinstance(arg_type, type(builtins.str)):
        return None

    try:
        statement_type = statement_type.last_known_value
    except Exception as e:
        # todo: check that it's error about bad fields
        print(e)

    return statement_type.value
