from collections import Counter
from sql_assignment_generator.constraints.base import BaseConstraint
from .base import SchemaConstraint
from sqlglot import Expression, exp 


class HasSamePrimaryKeyConstraint(SchemaConstraint):
    '''
    Requires that a specific number of tables share the SAME Primary Key column name.
    (e.g. Table A has PK "user_id" and Table B has PK "user_id").
    '''

    def __init__(self, min_tables: int = 2) -> None:
        self.min_tables = min_tables

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        pk_names = []

        for table in tables:
            schema = table.this
            if not isinstance(schema, exp.Schema):
                continue
            
            #look for inline pk
            for col_def in schema.find_all(exp.ColumnDef):
                col_name = col_def.this.output_name.lower()
                for constraint in col_def.args.get('constraints', []):
                    if isinstance(constraint.kind, exp.PrimaryKeyColumnConstraint):
                        pk_names.append(col_name)

            #look for pk table-level
            for expression in schema.expressions:
                if isinstance(expression, exp.PrimaryKey):
                    for col in expression.expressions:
                        pk_names.append(col.output_name.lower())

        #count all pk occurence by name
        pk_counts = Counter(pk_names)

        return any(count >= self.min_tables for count in pk_counts.values())
    
    @property
    def description(self) -> str:
        return f'{self.min_tables} tables must have the same PRIMARY KEY column name'
    
    def merge(self, other: SchemaConstraint) -> 'HasSamePrimaryKeyConstraint':
        if not isinstance(other, HasSamePrimaryKeyConstraint):
            raise ValueError("Cannot merge constraints of different types.")
        
        return HasSamePrimaryKeyConstraint(min_tables=max(self.min_tables, other.min_tables))