from .base import QueryConstraint
from sqlscope import Query
from ...exceptions import ConstraintValidationError

class NoGroupBy(QueryConstraint):
    '''Requires the absence of a GROUP BY clause.'''

    def validate(self, query: Query) -> None:
        #look for node GROUP BY in query
        for select in query.selects:
            if select.group_by is not None:
                raise ConstraintValidationError("Exercise requires grouping, which is not allowed.")
    
    @property
    def description(self) -> str:
        return "Exercise must not require grouping (i.e., no GROUP BY clause)."

class GroupBy(QueryConstraint):
    '''Requires the presence of a GROUP BY clause, optionally on a specified number of columns.'''

    def __init__(self, min_: int = 1, max_: int | None = None ) -> None:
        self.min = min_
        self.max = max_
    
    def validate(self, query: Query) -> None:
        # NOTE: in case multiple SELECTs (UNION/subqueries), the constraint is satisfied if ANY of them satisfy the constraint

        group_sizes: list[int] = []

        for select in query.selects:
            if select.group_by is None:
                continue
            group_sizes.append(len(select.group_by))

        # check if any group size satisfies the min/max condition
        for group_size in group_sizes:
            if self.max is None:
                if group_size >= self.min:
                    return
                continue
            if self.min <= group_size <= self.max:
                return
            continue

        raise ConstraintValidationError(
            "Exercise does not satisfy the GROUP BY column count requirements."
            f"GROUP BY column counts found: {group_sizes}, required min: {self.min}, required max: {self.max}"
        )

    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require grouping by at least {self.min} columns'
        if self.min == self.max:
            return f'Exercise must require grouping by exactly {self.min} columns'
        return f'Exercise must require grouping by between {self.min} and {self.max} columns'

