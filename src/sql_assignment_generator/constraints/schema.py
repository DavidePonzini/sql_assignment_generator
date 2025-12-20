from .base import BaseConstraint
from sqlglot import Expression, exp 

class TableAmountConstraint(BaseConstraint):
    '''Requires the schema to have a specific number of tables.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        table_count = len(tables)
        if self.max_tables < 0:
            return table_count >= self.min_tables
        return self.min_tables <= table_count <= self.max_tables
    
    @property
    def description(self) -> str:
        if self.max_tables < 0:
            return f'Must have minumum {self.min_tables} tables.'
        else:
            return f'Must have between {self.min_tables} and {self.max_tables} tables.'
        
class ColumnAmountConstraint(BaseConstraint):
    '''Requires each table in the schema to have a specific number of columns.'''

    def __init__(self, min_columns: int = 1) -> None:
        self.min_columns = min_columns

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        if not tables:
            return False
        
        for table in tables:
            # In sqlglot, l'espressione CREATE TABLE (exp.Create) contiene un oggetto 
            # 'Schema' (exp.Schema) nell'attributo .this
            schema = table.this

            if not isinstance(schema, exp.Schema):
                continue

            # Contiamo solo le definizioni di colonna (exp.ColumnDef).
            # Questo esclude automaticamente PRIMARY KEY separate, CONSTRAINT, CHECK, etc.
            column_count = sum(1 for e in schema.expressions if isinstance(e, exp.ColumnDef))
        
            if column_count < self.min_columns:
                return False
        return True

    @property
    def description(self) -> str:
        return f'Each table must have minumum {self.min_columns} columns.'
    
# class HasPrimaryKeyConstraint(BaseConstraint):
