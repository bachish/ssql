from typing import Callable, Optional

from messages import (
    any_type_args,
    cant_infer_query_statement,
    database_error,
    func_name,
)
from mypy.options import Options
from mypy.plugin import FunctionContext, Plugin
from mypy.typeops import try_getting_str_literals_from_type
from mypy.types import AnyType
from mypy.types import Type as MypyType
from mypy.types import get_proper_type
from ssql_psycopg2.pg_connection import PgConnection

#: Type for a function hook.
_FunctionCallback = Callable[[FunctionContext], MypyType]


class SsqlPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self.conn = PgConnection()

    def get_function_hook(
        self,
        fullname: str,
    ) -> Optional[_FunctionCallback]:
        def checker(ctx: FunctionContext) -> MypyType:
            statement: Optional[
                list[str]
            ] = try_getting_str_literals_from_type(ctx.arg_types[0][0])

            if statement is None or len(statement) == 0:
                ctx.api.msg.note(
                    cant_infer_query_statement(fullname), ctx.context
                )
                return ctx.default_return_type

            arg_types = []
            msg = None
            for idx in range(1, len(ctx.arg_types)):
                # TODO when need to check lists tail ?
                if len(ctx.arg_types[idx]) == 0:
                    arg_type = None
                else:
                    arg_type = ctx.arg_types[idx][0]

                proper_type = get_proper_type(arg_type)
                if isinstance(proper_type, AnyType):
                    ctx.api.msg.note(
                        any_type_args(idx + 1, fullname), ctx.context
                    )
                    msg = self.conn.check_without_types(statement[0])
                    if msg is not None:
                        ctx.api.fail(
                            database_error(fullname, msg), ctx.context
                        )
                    return ctx.default_return_type
                arg_types.append(proper_type)

            msg = self.conn.check(statement[0], arg_types)
            if msg is not None:
                ctx.api.fail(database_error(fullname, msg), ctx.context)

            return ctx.default_return_type

        if func_name(fullname) == "execute":
            return checker

        return None


def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    return SsqlPlugin
