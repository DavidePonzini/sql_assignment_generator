from collections import Counter
from sql_assignment_generator.constraints.base import BaseConstraint
from .base import SchemaConstraint
from sqlglot import Expression, exp 

class TableAmountConstraint(SchemaConstraint):
    '''Requires the schema to have a specific number of tables.'''

    def __init__(self, min_tables: int = 5) -> None:
        self.min_tables = min_tables

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        table_count = len(tables)
        return self.min_tables <= table_count

    @property
    def description(self) -> str:
        return f'Must have minimum {self.min_tables} TABLES'
    
    def merge(self, other: SchemaConstraint) -> 'TableAmountConstraint':
        if not isinstance(other, TableAmountConstraint):
            raise ValueError("Cannot merge constraints of different types.")
        
        return TableAmountConstraint(min_tables=max(self.min_tables, other.min_tables))