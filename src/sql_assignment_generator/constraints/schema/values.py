from collections import Counter
from .base import SchemaConstraint
from sqlglot import exp 
from ...exceptions import ConstraintMergeError
from sqlscope import Catalog


class MinRows(SchemaConstraint):
    '''Requires that EACH table found in the insert list has a specific minimum number of rows inserted.'''

    def __init__(self, min_: int = 3) -> None:
        self.min = min_

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> bool:
        table_row_counts = Counter()

        for value in values_sql:
            table_name = value.this.output_name.lower()
            values_node = value.expression

            # verify the format INSERT INTO ... VALUES ...
            if isinstance(values_node, exp.Values):     # list of insert row: (val1), (val2)...
                rows_in_statement = len(values_node.expressions)
                table_row_counts[table_name] += rows_in_statement

        # if no tables found but min > 0, fail
        if not table_row_counts and self.min > 0:
            return False

        # check each table meets minimum row requirement
        return all(count >= self.min for count in table_row_counts.values())
    
    @property
    def description(self) -> str:
        return f'Dataset must have at least {self.min} rows of data for each table.'
    
    def merge(self, other: SchemaConstraint) -> 'MinRows':
        if not isinstance(other, MinRows):
            raise ConstraintMergeError(self, other)
        
        min_rows = max(self.min, other.min)
        return MinRows(min_=min_rows)