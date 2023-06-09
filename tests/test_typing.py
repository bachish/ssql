import os
from typing import Final

from docker.models.containers import Container
from mypy import api

from ..ssql.messages import (
    any_type_args,
    cant_infer_query_statement,
    database_error,
)

checked_func: Final = "execute"

# TODO split into few test files (need fix docker creation)

#
# Test typing
#


def get_file_typing(name: str):
    return os.path.join(os.path.dirname(__file__), "resources", "typing", name)


def test_unknown_statement(postgres_container: Container):
    output, a, err_count = api.run(
        [get_file_typing("warn_cannot_get_statement.py")]
    )
    expected = cant_infer_query_statement(checked_func)
    assert expected in output


def test_anyType_arg(postgres_container: Container):
    output, a, err_count = api.run([get_file_typing("warn_anytype_arg.py")])
    expected = any_type_args(2, checked_func)
    assert expected in output


#
# Test database errors
#
def get_file_database(name: str):
    return os.path.join(
        os.path.dirname(__file__), "resources", "database", name
    )


def test_wrong_column(postgres_container: Container):
    output, a, err_count = api.run([get_file_database("wrong_column.py")])
    expected = database_error(checked_func, "")
    assert expected in output


def test_correct_types(postgres_container: Container):
    output, a, err_count = api.run(
        [get_file_database("correct_types_func.py")]
    )
    assert output == "" or "Success" in output


def test_correct_simple_query(postgres_container: Container):
    output, a, err_count = api.run([get_file_database("correct_simple.py")])
    assert output == "" or "Success" in output
