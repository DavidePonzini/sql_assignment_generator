import mysql.connector

from ..database import Database
from ..exceptions import QueryExecutionError

class MySQLDatabase(Database):
    def connect(self) -> None:
        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
        )

    def disconnect(self) -> None:
        self.connection.close()

    def execute_query(self, query: str) -> list[tuple]:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)

                if cursor.description is None:
                    return []

                results = cursor.fetchall()
            except mysql.connector.Error as err:
                raise QueryExecutionError(f'Error occurred while executing query: {err}') from err

        return [tuple(row) for row in results]
    
    def create_schema(self, schema: str) -> None:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(f'CREATE SCHEMA `{schema}`')
                cursor.execute(f'USE `{schema}`')
                
                super().create_schema(schema)
            except mysql.connector.Error as err:
                raise QueryExecutionError(f'Error occurred while creating schema: {err}') from err
            

    def delete_schema(self) -> None:
        if self.schema is None:
            return
        
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(f'DROP SCHEMA `{self.schema}`')
                
                super().delete_schema()
            except mysql.connector.Error as err:
                raise QueryExecutionError(f'Error occurred while deleting schema: {err}') from err