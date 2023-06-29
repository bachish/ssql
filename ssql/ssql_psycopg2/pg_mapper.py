import builtins
from typing import Dict, List, Optional

from core.mapper import Mapper, getTypeNameByInstance
from errors import SsqlTypeError
from messages import any_type_args_warn, unsupported_type
from mypy.types import AnyType, Instance, ProperType, TupleType


class PgMapper(Mapper):
    def __init__(self) -> None:
        self.PgTypes: Dict[str, str] = {
            builtins.int.__name__: "integer",
            builtins.bool.__name__: "boolean",
            builtins.str.__name__: "text",
            builtins.float.__name__: "real",
        }

    def get_type_name(self, var: Optional[ProperType]) -> str:
        if var is None:
            raise SsqlTypeError(unsupported_type(getTypeNameByInstance(var)))

        if isinstance(var, Instance):
            return self.PgTypes.get(getTypeNameByInstance(var))

        if isinstance(var, AnyType):
            raise SsqlTypeError(any_type_args_warn())

        raise SsqlTypeError(unsupported_type(getTypeNameByInstance(var)))

    def map_tuple(self, var: TupleType) -> str:
        return self.map_list(var.items)

    def map_list(self, vars: List[Optional[ProperType]]) -> str:
        return ",".join([self.get_type_name(arg) for arg in vars])

    def get_args_view(
        self, types: List[Optional[ProperType]]
    ) -> Optional[str]:
        if len(types) == 1 and isinstance(types[0], TupleType):
            return self.map_tuple(types[0])
        return self.map_list(types)
