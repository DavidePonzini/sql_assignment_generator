from .base import QueryConstraint
from sqlglot import exp
from sqlscope import Query
from ...exceptions import ConstraintValidationError

class NoHaving(QueryConstraint):
    '''Ensures that the query does not contain a HAVING clause.'''

    def validate(self, query: Query) -> None:
        for select in query.selects:
            if select.having is not None:
                raise ConstraintValidationError("Exercise must not require condition on groups (HAVING clause).")

    @property
    def description(self) -> str:
        return "Exercise must not require condition on groups (HAVING clause)."

class Having(QueryConstraint):
    '''
    Requires the presence (or absence) of a HAVING clause with a specific number of conditions.
    In case of multiple SELECTs (UNION/subqueries), the constraint is satisfied if ANY of them satisfy the constraint.
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        having_conditions: list[int] = []

        for select in query.selects:
            if select.having is None:
                continue

            conditions = 0
            # count main HAVING condition
            conditions += 1

            # count additional conditions connected by AND/OR
            conditions += len(list(select.having.find_all((exp.And, exp.Or))))

            having_conditions.append(conditions)

        # check if any having condition count satisfies the min/max condition
        for condition_count in having_conditions:
            if self.max is None:
                if condition_count >= self.min:
                    return
                continue
            if self.min <= condition_count <= self.max:
                return
            continue

        raise ConstraintValidationError(
            "Exercise does not satisfy the HAVING clause condition count requirements."
            f"HAVING clause condition counts found: {having_conditions}, required min: {self.min}, required max: {self.max}"
        )
    
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} logical conditions on a single group (HAVING clause).'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} logical conditions on a single group (HAVING clause).'
        return f'Exercise must require between {self.min} and {self.max} logical conditions on a single group (HAVING clause).'