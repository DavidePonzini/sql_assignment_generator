from collections import Counter
from .base import SchemaConstraint
from sqlglot import Expression, exp 


class ColumnAmountConstraint(SchemaConstraint):
    '''Requires that a specific number of tables in the schema have a minimum number of columns.'''

    def __init__(self, min_tables: int = 1, min_columns: int = 2) -> None:
        self.min_columns = min_columns
        self.min_tables = min_tables

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        if not tables:
            return False
        
        valid_tables_count = 0

        for table in tables:
            schema = table.this

            if not isinstance(schema, exp.Schema):
                continue

            # count columns in the table
            column_count = sum(1 for e in schema.expressions if isinstance(e, exp.ColumnDef))
            
            # IF column count meets the minimum, increment valid table count
            if column_count >= self.min_columns:
                valid_tables_count += 1
        
        return valid_tables_count >= self.min_tables

    @property
    def description(self) -> str:
        return f'At least {self.min_tables} tables must have minimum {self.min_columns} columns'

    def merge(self, other: SchemaConstraint) -> 'ColumnAmountConstraint':
        if not isinstance(other, ColumnAmountConstraint):
            raise ValueError("Cannot merge constraints of different types.")
        
        # Merging by taking the maximum of min_tables and min_columns
        merged_min_tables = max(self.min_tables, other.min_tables)
        merged_min_columns = max(self.min_columns, other.min_columns)

        return ColumnAmountConstraint(
            min_tables=merged_min_tables,
            min_columns=merged_min_columns
        )