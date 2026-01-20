from .base import QueryConstraint
from sqlglot import Expression, exp

class NoGroupBy(QueryConstraint):
    '''Requires the absence of a GROUP BY clause.'''

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        #look for node GROUP BY in query
        group_nodes = list(query_ast.find_all(exp.Group))
        return len(group_nodes) == 0
    
    @property
    def description(self) -> str:
        return "Exercise must NOT require grouping (i.e., no GROUP BY clause)."

class RequireGroupBy(QueryConstraint):
    '''Requires the presence (or absence) of a GROUP BY clause.'''

    def __init__(self, min_: int = 1, max_: int | None = None ) -> None:
        self.min = min_
        self.max = max_ if max_ is not None and max_ > min_ else None

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        groups = list(query_ast.find_all(exp.Group))
        
        if not groups:
            return False

        group_columns = 0
        for group in groups:
            group_columns += len(group.expressions)

        if self.max is None:
            return group_columns >= self.min
        return self.min <= group_columns <= self.max
    
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require grouping by at least {self.min} columns'
        if self.min == self.max:
            return f'Exercise must require grouping by exactly {self.min} columns'
        return f'Exercise must require grouping by between {self.min} and {self.max} columns'

