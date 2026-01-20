from collections import Counter
from .base import SchemaConstraint
from sqlglot import Expression, exp 


class HasSameColumnNameConstraint(SchemaConstraint):
    '''
    Requires that a specific number of tables share the SAME column name, excluding Primary Keys (non-key columns).
    '''

    def __init__(self, min_tables: int = 2) -> None:
        if min_tables < 2: min_tables = 2
        self.min_tables = min_tables

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        tables_non_key_cols = []

        for table in tables:
            schema = table.this
            if not isinstance(schema, exp.Schema):
                continue

            pk_cols = set()
            all_cols = set()

            # look for inline definitions (e.g. id INT PRIMARY KEY)
            for col_def in schema.find_all(exp.ColumnDef):
                col_name = col_def.this.output_name.lower()
                all_cols.add(col_name)
                
                for constraint in col_def.args.get('constraints', []):
                    if isinstance(constraint.kind, exp.PrimaryKeyColumnConstraint):
                        pk_cols.add(col_name)

            # look for table-level definitions (e.g. PRIMARY KEY (id))
            for expression in schema.expressions:
                if isinstance(expression, exp.PrimaryKey):
                    for col in expression.expressions:
                        pk_cols.add(col.output_name.lower())

            # keep only non-key columns and add to the list
            non_key_cols = all_cols - pk_cols
            if non_key_cols:
                tables_non_key_cols.append(non_key_cols)

        # count occurrences across all tables
        global_col_counter = Counter()
        for col_set in tables_non_key_cols:
            for col_name in col_set:
                global_col_counter[col_name] += 1

        return any(count >= self.min_tables for count in global_col_counter.values())

    @property
    def description(self) -> str:
        return f'In CREATE TABLE must have at least {self.min_tables} tables with non-key columns with EQUAL name'
