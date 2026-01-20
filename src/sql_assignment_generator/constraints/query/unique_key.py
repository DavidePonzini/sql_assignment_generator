from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp


class HasUniqueKeyConstraint(QueryConstraint):
    '''
    Checks for the presence of Primary Key or Unique Key columns in the SELECT clause.
    It analyzes the schema (tables) to identify keys and checks if they are selected in the query.

    Args:
        min_occurrences: Min occurrences required.
        max_occurrences: Max occurrences required (-1 for no limit).
        state: If True, must be present. If False, must NOT be present.
    '''

    def __init__(self, min_occurrences: int = 1, max_occurrences: int = -1, state: bool = True) -> None:
        self.min_occurrences = min_occurrences
        self.max_occurrences = max_occurrences if max_occurrences > min_occurrences else -1
        self.state = state

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        key_count = 0

        # 1. Identify primary keys and unique keys from schema tables
        pks = set()
        uks = set()

        for table in tables:
            schema = table.this
            if not isinstance(schema, exp.Schema): continue
            
            # Check all column definitions to find inline PK/UK (e.g., id INT PRIMARY KEY)
            for col_def in schema.find_all(exp.ColumnDef):
                col_name = col_def.this.output_name.lower()
                for inline_constraint in col_def.args.get('constraints', []): 
                    if isinstance(inline_constraint.kind, exp.PrimaryKeyColumnConstraint): 
                        pks.add(col_name)
                    elif isinstance(inline_constraint.kind, exp.UniqueColumnConstraint): 
                        uks.add(col_name)

            # Check definition of PK/UK at the end of CREATE TABLE (e.g. PRIMARY KEY (col1, col2))
            for constraint in schema.expressions:
                if isinstance(constraint, exp.PrimaryKey):
                    for col in constraint.expressions:
                        pks.add(col.output_name.lower())
                elif isinstance(constraint, exp.Constraint):
                    if isinstance(constraint.kind, exp.UniqueColumnConstraint):
                        if constraint.this:
                            cols = constraint.this.expressions if hasattr(constraint.this, 'expressions') else [constraint.this]
                            for col in cols:
                                if isinstance(col, exp.Column):
                                    uks.add(col.output_name.lower())
                                elif isinstance(col, exp.Identifier):
                                    uks.add(col.this.lower())

        valid_keys = pks.union(uks) # Accept both Primary Keys and Unique Keys

        # 2. Analyze SELECT clause to count how many valid keys are selected
        for select_node in query_ast.find_all(exp.Select):
            for expression in select_node.expressions:
                found_cols = []
                
                if isinstance(expression, exp.Column):
                    found_cols.append(expression.output_name.lower())
                # Case alias: check the original column (e.g., col AS alias)
                elif isinstance(expression, exp.Alias):
                    for col in expression.this.find_all(exp.Column):
                        found_cols.append(col.output_name.lower())
                else: # Case functions or complex expressions (e.g., SELECT COUNT(id))
                    for col in expression.find_all(exp.Column):
                        found_cols.append(col.output_name.lower())
                
                # Check if any found column is a key
                for col_name in found_cols:
                    if col_name in valid_keys:
                        key_count += 1
                        break # Count only once per select expression
        
        if not self.state: 
            return key_count == 0
        else: 
            return self.min_occurrences <= key_count <= self.max_occurrences if self.max_occurrences > 0 else self.min_occurrences <= key_count

    @property
    def description(self) -> str:
        elem_name = "PRIMARY or UNIQUE KEY in SELECT"
        if not self.state: return f"Must NOT have {elem_name}"
        
        if self.max_occurrences < 0: return f'Must have minimum {self.min_occurrences} {elem_name}'
        elif self.min_occurrences == self.max_occurrences: return f'Must have exactly {self.min_occurrences} {elem_name}'
        else: return f'Must have between {self.min_occurrences} and {self.max_occurrences} {elem_name}'