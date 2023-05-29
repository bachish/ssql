from typing import Callable

from mypy.plugin import FunctionContext, Plugin
from mypy.types import Type
#from ssql.plugin.helper import bar
class CustomPlugin(Plugin):

    def get_function_hook(
        self, fullname: str
    ) -> Callable[[FunctionContext], Type] | None:
        def checker(ctx: FunctionContext):
            ctx.api.fail("I FOUND SSQL ERROR!" , ctx.context)
            #ctx.api.fail("I FOUND SSQL ERROR!" + bar(), ctx.context)
            return ctx.default_return_type
        if fullname.endswith("query"):
            return checker
        
        return None


def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    return CustomPlugin
