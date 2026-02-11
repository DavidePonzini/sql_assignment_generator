from .base import QueryConstraint
from sqlglot import exp, parse_one
from sqlscope import Query
from ...exceptions import ConstraintValidationError

class NoOrderBy(QueryConstraint):
    '''Requires the absence of an ORDER BY clause.'''

    def validate(self, query: Query) -> None:
        selects_collection = query.selects.values() if hasattr(query.selects, 'values') else query.selects 

        for s in selects_collection:
            curr_select = s[1] if isinstance(s, tuple) else s
            if isinstance(curr_select, str): continue 

            ob = curr_select.order_by
            if ob is not None:
                if isinstance(ob, list):
                    if len(ob) > 0:
                        raise ConstraintValidationError("Exercise must not have an ordering, NO ORDER BY.")
                elif hasattr(ob, 'expressions'):
                    if len(ob.expressions) > 0:
                        raise ConstraintValidationError("Exercise must not have an ordering, NO ORDER BY.")
                else:
                    raise ConstraintValidationError("Exercise must not have an ordering, NO ORDER BY.")
    
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
        ast = parse_one(query.sql)
        order_nodes = list(ast.find_all(exp.Order))
        
        if not order_nodes:
            raise ConstraintValidationError("No ORDER BY clause found, but at least one DESC column is required.")

        for order_node in order_nodes:
            desc_count = 0
            for ordered_exp in order_node.expressions:
                #controll if the expression has the 'desc' attribute set to True
                if ordered_exp.args.get("desc") is True:
                    desc_count += 1
            
            if self.max is None:
                if desc_count >= self.min: return
            elif self.min <= desc_count <= self.max: return

        raise ConstraintValidationError(
            f"Exercise does not satisfy the ORDER BY DESC requirements. "
            f"Found {desc_count} descending columns, but required min: {self.min}. "
            "Make sure to explicitly use the DESC keyword in the SQL query."
        )
    
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} columns in ORDER BY to be in descending order.'
        elif self.min == self.max:
            return f'Exercise must require exactly {self.min} columns in ORDER BY to be in descending order.'
        else:
            return f'Exercise must require between {self.min} and {self.max} columns in ORDER BY to be in descending order.'