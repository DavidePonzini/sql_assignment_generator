from .base import QueryConstraint
from sqlglot import Expression, exp
from sql_error_categorizer.query import Query

class NoAlias(QueryConstraint):
    '''
    Requires that no columns in the SELECT clause are renamed (no aliases for columns).
    '''

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # find the main SELECT node
        query = Query(query_ast.sql())
        output = query.main_query.output

        for col in output.columns:
            if col.name != col.real_name:
                return False
        return True

    @property
    def description(self) -> str:
        return "Columns in SELECT must not be renamed (must not use aliases)"

class RequireAlias(QueryConstraint):
    '''
        Requires a number of columns in the SELECT clause to be renamed using an alias (AS).
    '''

    def __init__(self, min_: int, max_: int | None) -> None:
        super().__init__()
        self.min = min_
        self.max = max_


    def validate(self, query: Query) -> bool:
        # find the main SELECT node
        output = query.main_query.output

        alias_count = 0
        for col in output.columns:
            if col.name != col.real_name:
                alias_count += 1

        if self.max is None:
            return alias_count >= self.min
        return self.min <= alias_count <= self.max

    @property
    def description(self) -> str:
        if self.max is None:
            return f"At least {self.min} columns in SELECT must be renamed using an alias (AS)"
        if self.min == self.max:
            return f"Exactly {self.min} columns in SELECT must be renamed using an alias (AS)"
        return f"Between {self.min} and {self.max} columns in SELECT must be renamed using an alias (AS)"