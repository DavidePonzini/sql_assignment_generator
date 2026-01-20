from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp


class HasDistinctConstraint(QueryConstraint):
    '''
    Checks for the presence (or absence) of the DISTINCT keyword in the query.

    Args:
        min_occurrences: Min occurrences required.
        max_occurrences: Max occurrences required (-1 for no limit).
        state: If True, must be present. If False, must NOT be present.
    '''

    def __init__(self, min_occurrences: int = 1, max_occurrences: int = -1, state: bool = True) -> None:
        self.min_occurrences = min_occurrences
        self.max_occurrences = max_occurrences if max_occurrences > min_occurrences else -1
        self.state = state

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # Find all DISTINCT nodes
        distinct_nodes = list(query_ast.find_all(exp.Distinct))
        distinct_count = len(distinct_nodes)

        if not self.state: 
            return distinct_count == 0
        else: 
            return self.min_occurrences <= distinct_count <= self.max_occurrences if self.max_occurrences > 0 else self.min_occurrences <= distinct_count
    
    @property
    def description(self) -> str:
        if not self.state: return "Must NOT have DISTINCT keyword"
        
        if self.max_occurrences < 0: return f'Must have minimum {self.min_occurrences} DISTINCT keyword'
        elif self.min_occurrences == self.max_occurrences: return f'Must have exactly {self.min_occurrences} DISTINCT keyword'
        else: return f'Must have between {self.min_occurrences} and {self.max_occurrences} DISTINCT keyword'