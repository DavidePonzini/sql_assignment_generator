from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from ..costraintType import WhereConstraintType, DistinctOrUKInSelectConstraintType, AggregationConstraintType


class HasHavingConstraint(QueryConstraint):
    '''Requires the presence (or absence) of a HAVING clause with a specific number of conditions.'''

    def __init__(self, min_conditions: int = 1, max_conditions: int = -1, state: bool = True) -> None:
        self.min_conditions = min_conditions
        self.max_conditions = max_conditions if max_conditions > min_conditions else -1
        self.state = state

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # look for all node of HAVING in query
        having_nodes = list(query_ast.find_all(exp.Having))
        
        if having_nodes: 
            # take main HAVEING found
            having_node = having_nodes[0]
            conditions_count = 1
            conditions_count += len(list(having_node.find_all(exp.And)))
            conditions_count += len(list(having_node.find_all(exp.Or)))

            if not self.state: # case must NOT have HAVING
                return False
            else: # case must have HAVEING 
                if self.max_conditions < 0: return conditions_count >= self.min_conditions
                else:  return self.min_conditions <= conditions_count <= self.max_conditions
        else: # no HAVING found
            if not self.state: return True
            else: return False
    
    @property
    def description(self) -> str:
        if not self.state: return "Must NOT have HAVING clause"
        if self.max_conditions < 0: return f'Must have minimum {self.min_conditions} conditions in HAVING clause'
        elif self.min_conditions == self.max_conditions: return f'Must have exactly {self.min_conditions} conditions in HAVING clause'
        else: return f'Must have between {self.min_conditions} and {self.max_conditions} conditions in HAVING clause'

