import builtins
from typing import Dict

from mypy.types import (
    AnyType,
    CallableArgument,
    Instance,
    ProperType,
    TypeList,
    TypeVarLikeType,
    UnboundType,
)

from ssql.core.mapper import Mapper, getTypeNameByInstance


class PgMapper(Mapper):
    def __init__(self) -> None:
        self.PgTypes: Dict[str, str] = {
            builtins.int.__name__: "integer",
            builtins.bool.__name__: "boolean",
            builtins.str.__name__: "text",
        }

    def get_type_name(self, var: ProperType) -> str:
        if isinstance(var, Instance):
            try:
                type = self.PgTypes.get(getTypeNameByInstance(var))
                if type is None:
                    raise Exception("unknown type")
                return type
            except ValueError:
                raise Exception("unsupported type")

        if isinstance(var, TypeVarLikeType):
            pass
        if isinstance(var, UnboundType):
            pass
        if isinstance(var, CallableArgument):
            pass
        if isinstance(var, TypeList):
            pass
        if isinstance(var, AnyType):
            pass

        raise Exception("unsupported type")

    def map(self, some_type: ProperType) -> str:
        x = self.get_type_name(some_type)
        return x
