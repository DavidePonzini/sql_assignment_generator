from .base import QueryConstraint
from sqlglot import exp
from sqlscope import Query
from ...exceptions import ConstraintValidationError

class NoOrderBy(QueryConstraint):
    '''Requires the absence of an ORDER BY clause.'''

    def validate(self, query: Query) -> None:
        for select in query.selects:
            if select.order_by is not None:
                raise ConstraintValidationError("Exercise must not require ordering (i.e., no ORDER BY clause).")
    
    @property
    def description(self) -> str:
        return "Exercise must not require ordering (i.e., no ORDER BY clause)."

class OrderBy(QueryConstraint):
    '''
    Requires the presence of an ORDER BY clause with a specific number of columns.
    Ordering can be ascending or descending.
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def find_order_bys(self, query: Query) -> list[list[bool]]:
        '''
        Finds the number of columns in each ORDER BY clause within the query.

        Returns:
            A list of lists, where each inner list contains booleans indicating
            whether each column in the ORDER BY clause is ascending (True) or descending (False).
        '''

        order_bys: list[list[bool]] = []

        for select in query.selects:
            if select.order_by is None:
                continue

            order_by_columns: list[bool] = []
            for order in select.order_by:
                # Determine if the ordering is ascending (True) or descending (False)
                is_ascending = True
                if isinstance(order, exp.Ordered):
                    if order.desc:
                        is_ascending = False
                order_by_columns.append(is_ascending)

            order_bys.append(order_by_columns)

        return order_bys
    
    def validate(self, query: Query) -> None:
        order_bys = self.find_order_bys(query)

        for order_by in order_bys:
            count = len(order_by)

            if self.max is None:
                if count >= self.min:
                    return
                continue
            if self.min <= count <= self.max:
                return
            continue

        raise ConstraintValidationError(
            "Exercise does not satisfy the ORDER BY clause column count requirements."
            f"ORDER BY clause column counts found: {[len(ob) for ob in order_bys]}, required min: {self.min}, required max: {self.max}"
        )
    
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require ordering by at least {self.min} columns.'
        elif self.min == self.max:
            return f'Exercise must require ordering by exactly {self.min} columns.'
        else:
            return f'Exercise must require ordering by between {self.min} and {self.max} columns.'
        
class OrderByASC(OrderBy):
    '''
    Requires a certain number of columns in the ORDER BY clause to be in ascending order.
    '''

    def validate(self, query: Query) -> None:
        order_bys = self.find_order_bys(query)

        for order_by in order_bys:
            asc_count = sum(1 for is_asc in order_by if is_asc)

            if self.max is None:
                if asc_count >= self.min:
                    return
                continue
            if self.min <= asc_count <= self.max:
                return
            continue

        raise ConstraintValidationError(
            "Exercise does not satisfy the ORDER BY clause column count requirements."
            f"ORDER BY clause column counts found: {[len(ob) for ob in order_bys]}, required min: {self.min}, required max: {self.max}"
            "Only ascending columns are counted."
        )
    
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} columns in ORDER BY to be in ascending order.'
        elif self.min == self.max:
            return f'Exercise must require exactly {self.min} columns in ORDER BY to be in ascending order.'
        else:
            return f'Exercise must require between {self.min} and {self.max} columns in ORDER BY to be in ascending order.'
        
class OrderByDESC(OrderBy):
    '''
    Requires a certain number of columns in the ORDER BY clause to be in descending order.
    '''

    def validate(self, query: Query) -> None:
        order_bys = self.find_order_bys(query)

        for order_by in order_bys:
            desc_count = sum(1 for is_asc in order_by if not is_asc)

            if self.max is None:
                if desc_count >= self.min:
                    return
                continue
            if self.min <= desc_count <= self.max:
                return
            continue

        raise ConstraintValidationError(
            "Exercise does not satisfy the ORDER BY clause column count requirements."
            f"ORDER BY clause column counts found: {[len(ob) for ob in order_bys]}, required min: {self.min}, required max: {self.max}"
            "Only descending columns are counted."
        )
    
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} columns in ORDER BY to be in descending order.'
        elif self.min == self.max:
            return f'Exercise must require exactly {self.min} columns in ORDER BY to be in descending order.'
        else:
            return f'Exercise must require between {self.min} and {self.max} columns in ORDER BY to be in descending order.'