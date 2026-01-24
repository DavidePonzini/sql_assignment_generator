from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from sqlscope import Query

class NoSubquery(QueryConstraint):
    '''Requires the absence of subqueries in the SQL query.'''

    def validate(self, query: Query) -> bool:

        for select in query.selects:
            if len(select.subqueries) > 0:
                return False
        return True

    @property
    def description(self) -> str:
        return "Exercise must not require any subqueries."

class RequireUnnestedSubqueries(QueryConstraint):
    '''Requires the presence of a certain number of unnested subqueries in the SQL query.'''
    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> bool:
        unnested_subquery_counts = [len(select.subqueries) for select in query.selects]

        for count in unnested_subquery_counts:
            if self.max is None:
                if count >= self.min:
                    return True
                continue
            if self.min <= count <= self.max:
                return True
            continue

        return False

    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} unnested subqueries.'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} unnested subqueries.'
        return f'Exercise must require between {self.min} and {self.max} unnested subqueries.'

class RequireSubqueries(QueryConstraint):
    '''Requires the presence of nested subqueries (a subquery inside another subquery).'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> bool:
        nested_counts = []
        
        for select in query.selects:
            current_nesting_count = 0
            for subquery in select.subqueries:
                if len(subquery.subqueries) > 0:
                    current_nesting_count += 1
            nested_counts.append(current_nesting_count)

        for count in nested_counts:
            if self.max is None:
                if count >= self.min: return True
                continue
            if self.min <= count <= self.max: return True
            continue
        return False

    @property
    def description(self) -> str:
        if self.max is None: return f'Exercise must require at least {self.min} nested subqueries.'
        if self.min == self.max: return f'Exercise must require exactly {self.min} nested subqueries.'
        return f'Exercise must require between {self.min} and {self.max} nested subqueries.'