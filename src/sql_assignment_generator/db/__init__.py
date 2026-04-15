from .database import Database
from .drivers.postgresql import PostgresqlDatabase
from .drivers.mysql import MySQLDatabase
from .exceptions import QueryExecutionError

def get_database(host: str, port: int, user: str, password: str, dbms: str) -> Database:
    '''Factory function to get the appropriate database backend.'''

    if dbms == 'postgres':
        return PostgresqlDatabase(host, port, user, password)

    if dbms == 'mysql':
        return MySQLDatabase(host, port, user, password)

    raise ValueError(f'Unsupported DBMS: {dbms} ({host}:{port})')
