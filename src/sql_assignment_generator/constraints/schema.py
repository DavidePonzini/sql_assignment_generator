from .base import BaseConstraint
from sqlglot import Expression

class TableAmountConstraint(BaseConstraint):
    '''Requires the schema to have a specific number of tables.'''

    def __init__(self, min_tables: int, max_tables: int = -1) -> None:
        self.min_tables = min_tables
        if max_tables < 0:
            self.max_tables = min_tables
        else:
            self.max_tables = max_tables

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        table_count = len(tables)
        return self.min_tables <= table_count <= self.max_tables
    
    @property
    def description(self) -> str:
        if self.min_tables == self.max_tables:
            return f'Must have exactly {self.min_tables} tables.'
        else:
            return f'Must have between {self.min_tables} and {self.max_tables} tables.'
        
class ColumnAmountConstraint(BaseConstraint):
    '''Requires each table in the schema to have a specific number of columns.'''

    def __init__(self, min_columns: int, max_columns: int = -1) -> None:
        self.min_columns = min_columns
        if max_columns < 0:
            self.max_columns = min_columns
        else:
            self.max_columns = max_columns

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # TODO
        return True

    @property
    def description(self) -> str:
        if self.min_columns == self.max_columns:
            return f'Each table must have exactly {self.min_columns} columns.'
        else:
            return f'Each table must have between {self.min_columns} and {self.max_columns} columns.'