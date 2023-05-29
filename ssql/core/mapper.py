from mypy.nodes import TypeInfo
from mypy.types import Instance


class Mapper:
    @staticmethod
    def getTypeNameByInstance(var: Instance) -> str:
        # TODO it's unsafe type checking, fix is possible
        ti: TypeInfo = var.type
        return ti.name
