from abc import ABC, abstractmethod
from typing import Any
import time


class Database(ABC):
    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.schema: str | None = None

    def __enter__(self) -> 'Database':
        self.connect()
        
        self.create_schema(f'sql_assignment_generator_{time.time_ns()}')
        
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            self.delete_schema()
        except Exception as err:
            pass
        finally:
            self.disconnect()

    @abstractmethod
    def create_schema(self, schema: str) -> None:
        '''Create a new schema in the database and set it as the search path.'''
        self.schema = schema

    @abstractmethod
    def delete_schema(self) -> None:
        '''Delete the current schema from the database.'''
        if self.schema is not None:
            self.schema = None

    @abstractmethod
    def execute_query(self, query: str) -> list[tuple]:
        pass

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
