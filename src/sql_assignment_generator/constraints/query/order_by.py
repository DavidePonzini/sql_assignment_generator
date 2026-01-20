from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from ..costraintType import WhereConstraintType, DistinctOrUKInSelectConstraintType, AggregationConstraintType


class HasOrderByConstraint(QueryConstraint):
    '''Requires the presence (or absence) of an ORDER BY clause with a specific number of columns.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, state: bool = True) -> None:
        self.min_columns = min_tables
        self.max_columns = max_tables if max_tables > min_tables else -1
        self.state = state

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        order_by_nodes = list(query_ast.find_all(exp.Order))
        
        if order_by_nodes: 
            order_node = order_by_nodes[0]
            
            # extract number of columns in ORDER BY
            # order_node.expressions contains the list of columns in ORDER BY
            columns_in_order_by = len(order_node.expressions)

            if not self.state: # case: Must NOT have ORDER BY
                return False
            else: # case: Must have ORDER BY
                if self.max_columns < 0: return columns_in_order_by >= self.min_columns
                else: return self.min_columns <= columns_in_order_by <= self.max_columns
        else: # no ORDER BY found 
            if not self.state: return True
            else: return False
    
    @property
    def description(self) -> str:
        if not self.state: return "Must NOT have ORDER BY clause"
        
        if self.max_columns < 0: return f'Must have minimum {self.min_columns} columns in ORDER BY'
        elif self.min_columns == self.max_columns: return f'Must have exactly {self.min_columns} columns in ORDER BY'
        else: return f'Must have between {self.min_columns} and {self.max_columns} columns in ORDER BY'
