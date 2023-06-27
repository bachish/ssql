from typing import List, Optional

import psycopg2
import tomli
from core.connection import Connection
from errors import SsqlDBError
from mypy.types import ProperType
from ssql_psycopg2.pg_mapper import PgMapper

# TODO compare query and function arity


class PgConnection(Connection):
    """ """

    def __init__(self):
        self.mapper = PgMapper()
        connect = self.__read__()
        self.conn = psycopg2.connect(
            host=connect["host"],
            database=connect["database"],
            user=connect["user"],
            password=connect["password"],
        )

    def __read__(self):
        with open("pyproject.toml", "rb") as f:
            data = tomli.load(f)
            return data["ssql_postgres"]

    def check_without_types(self, query: str):
        """
        Check only syntax and semantic of statement.
        Can check only if query is a string value.
        """
        err = None
        try:
            curs = self.conn.cursor()
            # TODO it's unsafe argument passing, fix if possible
            curs.execute(f"PREPARE ssql_method as {query}")
            curs.execute("DEALLOCATE ssql_method")
        except psycopg2.DatabaseError as e:
            err = e

        self.conn.rollback()
        if err is not None:
            raise SsqlDBError(str(err))

    def check(self, query: str, types: List[Optional[ProperType]]):
        """
        Check statement with all or partition parameters types/
        Can check only if query is a string value.
        """
        err = None

        if len(types) == 0:
            return self.check_without_types(query)
        pgTypes = self.mapper.get_args_view(types)
        with self.conn.cursor() as curs:
            try:
                # TODO it's unsafe argument passing, fix if possible
                curs.execute(f"PREPARE ssql_method({pgTypes}) as {query}")
                curs.execute("DEALLOCATE ssql_method")
            except psycopg2.DatabaseError as e:
                err = e

        if err is not None:
            raise SsqlDBError(str(err))
