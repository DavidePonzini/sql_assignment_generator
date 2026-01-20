from collections import Counter

from sql_assignment_generator.constraints.base import BaseConstraint
from .base import SchemaConstraint
from sqlglot import Expression, exp 


class HasComplexColumnNameConstraint(SchemaConstraint):
    '''
    Requires that the schema contains a specific minimum number of "complex" and "longer" columns.
    A complex column is defined as having a name with length >= 15 characters 
    and containing at least one underscore separator ('_').
    '''

    def __init__(self, min_complex_cols: int = 1) -> None:
        self.min_complex_cols = min_complex_cols

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        complex_cols_found = 0

        for table in tables:
            schema = table.this
            if not isinstance(schema, exp.Schema):
                continue

            # look for all column definitions
            for col_def in schema.find_all(exp.ColumnDef):
                col_name = col_def.this.output_name
                
                # complexity an longth criteria that I want use
                if len(col_name) >= 15 and '_' in col_name:
                    complex_cols_found += 1

        return complex_cols_found >= self.min_complex_cols
    
    @property
    def description(self) -> str:
        return f'Must have at least {self.min_complex_cols} columns with complex and longer names (length >= 15 and containing "_")'

    def merge(self, other: SchemaConstraint) -> 'HasComplexColumnNameConstraint':
        if not isinstance(other, HasComplexColumnNameConstraint):
            raise ValueError("Cannot merge constraints of different types.")
        
        return HasComplexColumnNameConstraint(min_complex_cols=max(self.min_complex_cols, other.min_complex_cols))