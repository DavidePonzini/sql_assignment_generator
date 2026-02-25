from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
import sqlglot
from sqlscope import Query
from ...exceptions import ConstraintValidationError

class Union(QueryConstraint):
    '''
    Requires the presence of UNIONs (including UNION ALL).
    Can specify a minimum and maximum number of UNIONs.
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def count_unions(self, query: Query) -> tuple[int, int]:
        '''
        Counts the number of UNION and UNION ALL operations in the query.

        Returns:
            A tuple (union_count, union_all_count).
        '''

        union_count = 0
        union_all_count = 0

        sql = query.sql
        ast = sqlglot.parse_one(sql)
        for union_node in ast.find_all(exp.Union):
            if union_node.args.get("distinct"):
                union_count += 1
            else:
                union_all_count += 1

        return union_count, union_all_count


    def validate(self, query: Query) -> None:
        union_count, union_all_count = self.count_unions(query)
        total_unions = union_count + union_all_count

        if self.max is None:
            if total_unions < self.min:
                raise ConstraintValidationError(f'Exercise must require at least {self.min} UNION operations.')
        else:
            if not (self.min <= total_unions <= self.max):
                raise ConstraintValidationError(f'Exercise must require between {self.min} and {self.max} UNION operations.')
            
    
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} UNION operations.'
        elif self.min == self.max:
            return f'Exercise must require exactly {self.min} UNION operations.'
        else:
            return f'Exercise must require between {self.min} and {self.max} UNION operations.'
        
class NoUnion(Union):
    '''Ensures that the query does not contain any UNION operations.'''

    def __init__(self) -> None:
        super().__init__(min_=0, max_=0)

    @property
    def description(self) -> str:
        return "Exercise must not require combining results from multiple queries (i.e., no UNION operations)."

class UnionOfType(Union):
    '''
    Requires the presence of UNIONs of a specific type: either 'UNION' or 'UNION ALL'.
    
    Args:
        all (bool): If True, requires 'UNION ALL'. If False, requires 'UNION'.
        min (int): Minimum number of specified UNION type required. Default is 1.
        max (int | None): Maximum number of specified UNION type allowed. Default is None (no maximum).
    '''

    def __init__(self, all: bool, min_: int = 1, max_: int | None = None) -> None:
        super().__init__(min_, max_)
        self.all = all

    def validate(self, query: Query) -> None:
        union_count, union_all_count = self.count_unions(query)

        if self.all:    # 'UNION ALL'
            count = union_all_count
        else:           # 'UNION'
            count = union_count

        union_type = 'UNION ALL' if self.all else 'UNION'
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(f'Exercise must require at least {self.min} {union_type} operations.')
        else:
            if not (self.min <= count <= self.max):
                raise ConstraintValidationError(f'Exercise must require between {self.min} and {self.max} {union_type} operations.')
            
    @property
    def description(self) -> str:
        union_type = 'UNION ALL' if self.all else 'UNION'
        if self.max is None:
            return f'Exercise must require at least {self.min} {union_type} operations.'
        elif self.min == self.max:
            return f'Exercise must require exactly {self.min} {union_type} operations.'
        else:
            return f'Exercise must require between {self.min} and {self.max} {union_type} operations.'