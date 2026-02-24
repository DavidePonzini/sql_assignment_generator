from collections import Counter
from .base import SchemaConstraint
from sqlglot import exp 
from ...exceptions import ConstraintMergeError, ConstraintValidationError
from sqlscope import Catalog

import dav_tools

class MinRows(SchemaConstraint):
    '''Requires that EACH table found in the insert list has a specific minimum number of rows inserted.'''

    def __init__(self, min_: int = 3) -> None:
        self.min = min_

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        table_row_counts = Counter()

        for value in values_sql:

            table_name = value.this.this.name.lower()
            values_node = value.expression

            # verify the format INSERT INTO ... VALUES ...
            if isinstance(values_node, exp.Values):     # list of insert row: (val1), (val2)...
                rows_in_statement = len(values_node.expressions)
                table_row_counts[table_name] += rows_in_statement

        dav_tools.messages.debug(f"DEBUG: Row counts per table for MinRows constraint: {table_row_counts}")

        # if no tables found but min > 0, fail
        if not table_row_counts and self.min > 0:
            raise ConstraintValidationError(f'No rows found for any table, which is less than the required minimum of {self.min} rows per table.')

        # check each table meets minimum row requirement
        for table_name, count in table_row_counts.items():
            if count < self.min:
                raise ConstraintValidationError(f'Table "{table_name}" has {count} rows, which is less than the required minimum of {self.min} rows.')

    @property
    def description(self) -> str:
        return f'Dataset must have at least {self.min} rows of data for each table.'
    
    def merge(self, other: SchemaConstraint) -> 'MinRows':
        if not isinstance(other, MinRows):
            raise ConstraintMergeError(self, other)
        
        min_rows = max(self.min, other.min)
        return MinRows(min_=min_rows)