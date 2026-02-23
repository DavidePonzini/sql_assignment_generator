from .base import QueryConstraint
from sqlscope import Query
from ...exceptions import ConstraintValidationError

class NoGroupBy(QueryConstraint):
    '''Requires the absence of a GROUP BY clause.'''

    def validate(self, query: Query) -> None:
        for s in query.selects:
            curr_select = s[1] if isinstance(s, tuple) else s
            gb = curr_select.group_by

            if gb is not None:
                if isinstance(gb, list) and len(gb) > 0:
                    raise ConstraintValidationError(self.description)
                elif bool(gb):
                    raise ConstraintValidationError(self.description)
    
    @property
    def description(self) -> str:
        return "Exercise must not require grouping (i.e., no GROUP BY clause)."

class GroupBy(QueryConstraint):
    '''Requires the presence of a GROUP BY clause, optionally on a specified number of columns.'''

    def __init__(self, min_: int = 1, max_: int | None = None ) -> None:
        self.min = min_
        self.max = max_
    
    def validate(self, query: Query) -> None:
        for s in query.selects:
            curr_select = s[1] if isinstance(s, tuple) else s
            gb = curr_select.group_by
            size = 0

            if gb is not None:
                if isinstance(gb, list): size = len(gb)
                elif bool(gb): size = 1
            
            if size > 0:
                is_min_ok = size >= self.min
                is_max_ok = (self.max is None or size <= self.max)
                if is_min_ok and is_max_ok: return 

        raise ConstraintValidationError(
            "Exercise does not satisfy the GROUP BY column count requirements. "
            f"GROUP BY column required min: {self.min}, max: {self.max if self.max else 'unlimited'}"
        )

    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require grouping by at least {self.min} columns'
        if self.min == self.max:
            return f'Exercise must require grouping by exactly {self.min} columns'
        return f'Exercise must require grouping by between {self.min} and {self.max} columns'
