from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
import sqlglot
from sqlscope import Query

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
            if union_node.args.get("all"):
                union_all_count += 1
            else:
                union_count += 1

        return union_count, union_all_count


    def validate(self, query: Query) -> bool:
        union_count, union_all_count = self.count_unions(query)
        total_unions = union_count + union_all_count

        if self.max is None:
            return total_unions >= self.min
        return self.min <= total_unions <= self.max

    
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

    def validate(self, query: Query) -> bool:
        union_count, union_all_count = self.count_unions(query)

        if not self.all:  # 'UNION'
            count = union_count
        else:  # 'UNION ALL'
            count = union_all_count

        if self.max is None:
            return count >= self.min
        return self.min <= count <= self.max