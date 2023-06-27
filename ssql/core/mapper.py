from errors import SsqlTypeError
from messages import unsupported_type
from mypy.nodes import TypeInfo
from mypy.types import Instance


class Mapper:
    pass


def getTypeNameByInstance(var: Instance) -> str:
    # TODO it's unsafe type checking, fix is possible
    if isinstance(var.type, TypeInfo):
        return var.type.name
    raise SsqlTypeError(unsupported_type(str(var)))
