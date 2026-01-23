from .base import QueryConstraint
from sqlglot import Expression, exp
from sqlscope import Query

class RequireColumnNumber(QueryConstraint):
    '''Requires a specific number of columns in the main SELECT clause.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> bool:
        output = query.main_query.output

        columns = len(output.columns)

        if self.max is None:
            return columns >= self.min
        return self.min <= columns <= self.max
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Query must select at least {self.min} columns'
        if self.min == self.max:
            return f'Query must select exactly {self.min} columns'
        return f'Query must select between {self.min} and {self.max} columns'