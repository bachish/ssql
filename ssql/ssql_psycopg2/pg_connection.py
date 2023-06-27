from typing import List, Optional

import psycopg2
from core.connection import Connection
from errors import SsqlDBError
from mypy.types import ProperType
from ssql_psycopg2.pg_mapper import PgMapper

# TODO compare query and function arity


class PgConnection(Connection):
    """ """

    def __init__(self):
        self.mapper = PgMapper()
        # TODO remove connection properties from code
        self.conn = psycopg2.connect(
            host="172.17.0.2",
            database="postgres",
            user="postgres",
            password="123",
        )

    def check_without_types(self, query: str):
        """
        Check only syntax ans semantic of statement.
        Can check only if query is a string value.
        """
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    # TODO it's unsafe argument passing, fix if possible
                    curs.execute(f"PREPARE ssql_method as {query}")
                except psycopg2.DatabaseError as e:
                    raise SsqlDBError(str(e))
                self.conn.rollback()

    def check(self, query: str, types: List[Optional[ProperType]]):
        """
        In psycopg2 a context wraps a transaction:
        if the context exits with success the transaction is committed,
        if it exits with an exception the transaction is rolled back
        https://www.psycopg.org/docs/connection.html
        """
        if len(types) == 0:
            return self.check_without_types(query)
        pgTypes = self.mapper.get_args_view(types)
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    # TODO it's unsafe argument passing, fix if possible
                    curs.execute(f"PREPARE ssql_method({pgTypes}) as {query}")
                except psycopg2.DatabaseError as e:
                    raise SsqlDBError(str(e))
                self.conn.rollback()
