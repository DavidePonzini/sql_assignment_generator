from .base import QueryConstraint
from sqlglot import Expression, exp

class NoHaving(QueryConstraint):
    '''Ensures that the query does not contain a HAVING clause.'''

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        having = query_ast.find(exp.Having)

        return having is None

    @property
    def description(self) -> str:
        return "Exercise must not require condition on groups (HAVING clause)."

class RequireHaving(QueryConstraint):
    '''Requires the presence (or absence) of a HAVING clause with a specific number of conditions.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min_conditions = min_
        self.max = max_ if max_ is not None and max_ >= min_ else None

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # look for all node of HAVING in query
        havings = list(query_ast.find_all(exp.Having))
        
        if not havings:
            return False

        conditions = 0
        for having in havings:
            conditions += 1  # count main HAVING condition
            conditions += len(list(having.find_all((exp.And, exp.Or))))

        if self.max is None:
            return conditions >= self.min_conditions
        return self.min_conditions <= conditions <= self.max
    
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min_conditions} conditions on groups (HAVING clause).'
        if self.min_conditions == self.max:
            return f'Exercise must require exactly {self.min_conditions} conditions on groups (HAVING clause).'
        return f'Exercise must require between {self.min_conditions} and {self.max} conditions on groups (HAVING clause).'

