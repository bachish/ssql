from typing import Optional, Type

from mypy.typeops import try_getting_str_literals_from_type


def get_literal_str(typ: Type) -> Optional[list[str]]:
    res = try_getting_str_literals_from_type(typ)
    return res
