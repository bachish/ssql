import builtins
from typing import Dict

from core.mapper import Mapper
from mypy.types import (
    AnyType,
    CallableArgument,
    Instance,
    ProperType,
    TypeList,
    TypeVarLikeType,
    UnboundType,
)


class PgMapper(Mapper):
    def __init__(self) -> None:
        self.PgTypes: Dict[str, str] = {
            builtins.int.__name__: "integer",
            builtins.bool.__name__: "boolean",
            builtins.str.__name__: "text",
        }

    def get_string(self, var: ProperType) -> str:
        if isinstance(var, Instance):
            try:
                return self.PgTypes.get(Mapper.getTypeNameByInstance(var))
            except ValueError:
                print("unsupported type :(")

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

    def map(self, some_type: ProperType) -> str:
        x = self.get_string(some_type)
        return x
