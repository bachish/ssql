from typing import Callable, Optional

from errors import SsqlDBError, SsqlTypeError
from messages import (
    any_type_args_warn,
    cant_infer_query_statement,
    database_error,
    func_name,
)
from mypy.options import Options
from mypy.plugin import FunctionContext, Plugin
from mypy.types import AnyType
from mypy.types import Type as MypyType
from mypy.types import get_proper_type
from mypy_utils import get_literal_str
from ssql_psycopg2.pg_connection import PgConnection

#: Type for a function hook.
_FunctionCallback = Callable[[FunctionContext], MypyType]


class SsqlPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self.conn = PgConnection()

    def get_arg_type(self, arg_type):
        # TODO check None argument (it's may be a valid value)
        proper_type = get_proper_type(arg_type)
        if isinstance(proper_type, AnyType):
            raise SsqlTypeError(any_type_args_warn())
        return proper_type

    def get_function_hook(
        self,
        fullname: str,
    ) -> Optional[_FunctionCallback]:
        def checker(ctx: FunctionContext) -> MypyType:
            statement: Optional[list[str]] = get_literal_str(
                ctx.arg_types[0][0]
            )

            if statement is None or len(statement) == 0:
                ctx.api.msg.note(cant_infer_query_statement(), ctx.context)
                return ctx.default_return_type

            arg_types = []
            try:
                # try to get all args types
                for idx in range(1, len(ctx.arg_types)):
                    arg_list = ctx.arg_types[idx]
                    if len(arg_list) > 0:
                        # TODO when need to check lists tail ?
                        arg_type = self.get_arg_type(arg_list[0])
                        arg_types.append(arg_type)

            except SsqlTypeError as se:
                ctx.api.msg.note(se.msg, ctx.context)
                try:
                    self.conn.check_without_types(statement[0])
                except SsqlDBError as de:
                    ctx.api.fail(database_error(de.msg), ctx.context)
            try:
                self.conn.check(statement[0], arg_types)
            except SsqlDBError as de:
                ctx.api.fail(database_error(de.msg), ctx.context)

            return ctx.default_return_type

        if func_name(fullname) == "execute":
            return checker

        return None


def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    return SsqlPlugin
