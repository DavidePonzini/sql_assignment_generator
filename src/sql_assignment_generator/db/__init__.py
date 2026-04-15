from .database import Database
from .drivers.postgresql import PostgresqlDatabase
from .drivers.mysql import MySQLDatabase
from .exceptions import QueryExecutionError
import dav_tools


def get_database(host: str, port: int, user: str, password: str, dbms: str) -> Database:
    '''Factory function to get the appropriate database backend.'''

    if dbms == 'postgres':
        return PostgresqlDatabase(host, port, user, password)

    if dbms == 'mysql':
        return MySQLDatabase(host, port, user, password)

    dav_tools.messages.warning(f'Unsupported database system "{dbms}". Skipping SQL execution steps.')
    return DummyDatabase(host, port, user, password)


class DummyDatabase(Database):
    '''A dummy database implementation that does not actually connect to anything. Used for unsupported database systems.'''
    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def execute_query(self, query: str) -> list[tuple]:
        return []
    
    def create_schema(self, schema: str) -> None:
        super().create_schema(schema)

    def delete_schema(self) -> None:
        super().delete_schema()