'''Constraints related to database schema.'''

from collections import Counter
from .base import BaseConstraint
from sqlglot import Expression, exp 


class TableAmountConstraint(BaseConstraint):
    '''Requires the schema to have a specific number of tables.'''

    def __init__(self, min_tables: int = 5) -> None:
        self.min_tables = min_tables

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        table_count = len(tables)
        return self.min_tables <= table_count
    
    @property
    def description(self) -> str:
        return f'Must have minimum {self.min_tables} TABLES'
       
class ColumnAmountConstraint(BaseConstraint):
    '''Requires each table in the schema to have a specific number of columns.'''

    def __init__(self, min_columns: int = 2) -> None:
        self.min_columns = min_columns

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        if not tables:
            return False
        
        for table in tables:
            schema = table.this

            if not isinstance(schema, exp.Schema):
                continue

            column_count = sum(1 for e in schema.expressions if isinstance(e, exp.ColumnDef))
            if column_count < self.min_columns:
                return False
        return True

    @property
    def description(self) -> str:
        return f'Each table must have minimum {self.min_columns} columns'

class InsertAmountConstraint(BaseConstraint):
    '''Requires that EACH table found in the insert list has a specific minimum number of rows inserted.'''

    def __init__(self, min_rows: int = 3) -> None:
        self.min_rows = min_rows

    def validate(self, query_ast: list[Expression] | Expression, tables: list[Expression]) -> bool:
        table_row_counts = Counter()
        insert_nodes = []

        if isinstance(query_ast, list): insert_nodes = query_ast
        elif isinstance(query_ast, Expression): insert_nodes = list(query_ast.find_all(exp.Insert))

        for insert_node in insert_nodes:
            if not isinstance(insert_node, exp.Insert): continue
            if not insert_node.this: continue
                
            table_name = insert_node.this.output_name.lower()
            values_node = insert_node.expression

            #verify the format INSERT INTO ... VALUES ...
            if isinstance(values_node, exp.Values): #list of insert row: (val1), (val2)...
                rows_in_statement = len(values_node.expressions)
                table_row_counts[table_name] += rows_in_statement

        #no inserted row
        if not table_row_counts and self.min_rows > 0: return False

        #quantity controll
        for count in table_row_counts.values():
            if count < self.min_rows: return False
        return True
    
    @property
    def description(self) -> str:
        return f'Must insert minimum {self.min_rows} rows of data for each table.'

class HasSamePrimaryKeyConstraint(BaseConstraint):
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
    
class HasCheckConstraint(BaseConstraint):
    '''Requires the schema to have a specific number of CHECK constraints.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1) -> None:
        self.min_checks = min_tables
        self.max_checks = max_tables if max_tables > min_tables else -1

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        total_checks = 0
        
        for table in tables:
            checks_found = list(table.find_all(exp.Check, exp.CheckColumnConstraint))
            total_checks += len(checks_found)

        if self.max_checks < 0:
            return total_checks >= self.min_checks
        return self.min_checks <= total_checks <= self.max_checks
    
    @property
    def description(self) -> str:
        if self.max_checks < 0: 
            return f'Must have minimum {self.min_checks} CHECK constraints in schema'
        elif self.min_checks == self.max_checks: 
            return f'Must have exactly {self.min_checks} CHECK constraints in schema'
        else: 
            return f'Must have between {self.min_checks} and {self.max_checks} CHECK constraints in schema'
