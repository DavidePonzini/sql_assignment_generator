from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from ..costraintType import WhereConstraintType, DistinctOrUKInSelectConstraintType, AggregationConstraintType


class HasGroupByConstraint(QueryConstraint):
    '''Requires the presence (or absence) of a GROUP BY clause.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, state: bool = True) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1
        
        self.state = state

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        #look for alla node GROUP BY in query
        group_nodes = list(query_ast.find_all(exp.Group))
        count = len(group_nodes)

        if not self.state: #case: Must NOT have GROUP BY
            return count == 0
        else: #case: Must have GROUP BY
            return count >= self.min_tables if self.max_tables == -1 else self.min_tables <= count <= self.max_tables
    
    @property
    def description(self) -> str:
        if self.state == False:
            return "Must NOT have GROUP BY"
        
        if self.max_tables < 0: return f'Must have minimum {self.min_tables} GROUP BY'
        elif self.min_tables == self.max_tables: return f'Must have exactly {self.min_tables} GROUP BY'
        else: return f'Must have between {self.min_tables} and {self.max_tables} GROUP BY'
