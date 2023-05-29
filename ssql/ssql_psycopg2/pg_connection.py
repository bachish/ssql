import psycopg2
from core.connection import Connection
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

    def check_without_types(self, query) -> str | None:
        """
        Check only syntax ans semantic of statement.
        Can check only if query is a string value.
        """
        msg = None
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    # TODO it's unsafe argument passing, fix if possible
                    curs.execute(f"""PREPARE ssql_method as {query}""")
                except psycopg2.DatabaseError as e:
                    msg = str(e)
                self.conn.rollback()
        return msg

    def check(self, query, types: ProperType) -> str | None:
        """
        In psycopg2 a context wraps a transaction:
        if the context exits with success the transaction is committed,
        if it exits with an exception the transaction is rolled back
        https://www.psycopg.org/docs/connection.html
        """
        pgTypes = ",".join([self.mapper.map(x) for x in types])
        msg = None
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    # TODO it's unsafe argument passing, fix if possible
                    curs.execute(
                        f"""PREPARE ssql_method({pgTypes}) as {query}"""
                    )
                except psycopg2.DatabaseError as e:
                    msg = str(e)
                self.conn.rollback()
        return msg
