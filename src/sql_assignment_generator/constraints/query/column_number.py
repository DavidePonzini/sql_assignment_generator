from .base import QueryConstraint
from sqlglot import Expression, exp

class RequireColumnNumber(QueryConstraint):
    '''Requires a specific number of columns in the main SELECT clause.'''

    def __init__(self, min_columns: int = 1, max_columns: int = -1) -> None:
        self.min_columns = min_columns
        self.max_columns = max_columns if max_columns >= min_columns else -1

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # look for main select
        select_node = query_ast if isinstance(query_ast, exp.Select) else query_ast.find(exp.Select)

        if not select_node: return False

        # select_node.expressions contain all column in select
        actual_count = len(select_node.expressions)

        if self.max_columns < 0: return actual_count >= self.min_columns
        return self.min_columns <= actual_count <= self.max_columns

    @property
    def description(self) -> str:
        if self.max_columns < 0: return f'Must select minimum {self.min_columns} columns'
        elif self.min_columns == self.max_columns: return f'Must select exactly {self.min_columns} columns'
        else: return f'Must select between {self.min_columns} and {self.max_columns} columns'