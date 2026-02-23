from .base import QueryConstraint
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
        having_condition_counts: list[int] = []

        for s in query.selects:
            curr_select = s[1] if isinstance(s, tuple) else s
            if not hasattr(curr_select, 'having') or curr_select.having is None: continue

            connectors = 0
            for node in curr_select.having.walk():
                if hasattr(node, 'key') and node.key in ('and', 'or'): connectors += 1
            
            having_condition_counts.append(1 + connectors)

        if not having_condition_counts:
            raise ConstraintValidationError("No HAVING clause found in the query.")
            
        for count in having_condition_counts:
            if count < self.min or (self.max is not None and count > self.max):
                raise ConstraintValidationError(
                    "Exercise does not satisfy the HAVING clause condition count requirements. "
                    f"required min: {self.min}, max: {self.max if self.max else 'unlimited'}."
                )
    
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} logical conditions on a single group (HAVING clause).'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} logical conditions on a single group (HAVING clause).'
        return f'Exercise must require between {self.min} and {self.max} logical conditions on a single group (HAVING clause).'