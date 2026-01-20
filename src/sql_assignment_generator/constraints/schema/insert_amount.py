from collections import Counter
from .base import SchemaConstraint
from sqlglot import Expression, exp 


class InsertAmountConstraint(SchemaConstraint):
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
    