from collections import Counter

from sql_assignment_generator.exceptions import ConstraintValidationError
from .base import QueryConstraint
from sqlglot import Expression, exp
from sqlscope import Query

class NoSubquery(QueryConstraint):
    '''Requires the absence of subqueries in the SQL query.'''

    def validate(self, query: Query) -> bool:

        for select in query.selects:
            if len(select.subqueries) > 0:
                raise ConstraintValidationError(
                    "Subqueries were detected in the solution, but this exercise must be solved "
                    "without using any subqueries."
                )

    @property
    def description(self) -> str:
        return "Exercise must not require any subqueries."

class UnnestedSubqueries(QueryConstraint):
    '''Requires the presence of a certain number of unnested subqueries in the SQL query.'''
    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> bool:
        unnested_subquery_counts = [len(select.subqueries) for select in query.selects]

        for count in unnested_subquery_counts:
            if self.max is None:
                if count >= self.min:
                    return
                continue
            if self.min <= count <= self.max:
                return
            continue

        raise ConstraintValidationError(
            f"Number of unnested subqueries is insufficient. Found counts per SELECT: {unnested_subquery_counts}. "
            f"Requirements: min={self.min}, max={self.max}"
        )

    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} unnested subqueries.'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} unnested subqueries.'
        return f'Exercise must require between {self.min} and {self.max} unnested subqueries.'

class Subqueries(QueryConstraint):
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
                if count >= self.min: return
                continue
            if self.min <= count <= self.max: return
            continue
        raise ConstraintValidationError(
            f"Insufficient nesting level for subqueries. Found {nested_counts} nested subqueries, "
            f"but the exercise requires min={self.min} and max={self.max} nested structures."
        )

    @property
    def description(self) -> str:
        if self.max is None: return f'Exercise must require at least {self.min} nested subqueries.'
        if self.min == self.max: return f'Exercise must require exactly {self.min} nested subqueries.'
        return f'Exercise must require between {self.min} and {self.max} nested subqueries.'