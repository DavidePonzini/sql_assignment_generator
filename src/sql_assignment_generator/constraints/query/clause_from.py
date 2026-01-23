from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from sqlscope import Query

class RequireTableReferences(QueryConstraint):
    '''
    Requires the query to reference a specified number of different tables (either in FROM or JOIN clauses).
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> bool:
        referenced_tables: set[str] = set()

        for select in query.selects:
            for table in select.referenced_tables:
                referenced_tables.add(table.real_name)

        table_count = len(referenced_tables)
        if self.max is None:
            return table_count >= self.min
        return self.min <= table_count <= self.max
    
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require referencing at least {self.min} different tables (i.e., JOINs).'
        elif self.min == self.max:
            return f'Exercise must require exactly {self.min} tables (i.e., JOINs).'
        else:
            return f'Exercise must require between {self.min} and {self.max} tables (i.e., JOINs).'


class RequireJoin(QueryConstraint):
    '''
    Requires the presence of JOINs.
    Can specify if strictly LEFT, RIGHT, or generic JOINs are required.
    '''

    def __init__(self, min_: int = 1, max_: int = -1, left: bool = False, right: bool = False) -> None:
        self.min = min_
        self.max = max_
        self.left = left
        self.right = right

    def validate(self, query: Query) -> bool:
        count = 0
        #found all join nodes
        for join_node in query_ast.find_all(exp.Join):
            join_kind = (join_node.kind or "").upper()
            join_side = (join_node.side or "").upper()

            is_left = 'LEFT' in join_kind or 'LEFT' in join_side
            is_right = 'RIGHT' in join_kind or 'RIGHT' in join_side

            if self.left and self.right: #case both LEFT and RIGHT
                if is_left or is_right: count += 1
            elif self.left: #case only LEFT
                if is_left: count += 1
            elif self.right: #case only RIGHT
                if is_right: count += 1
            else: count += 1

        if self.max < 0:
            return count >= self.min
        return self.min <= count <= self.max
    
    @property
    def description(self) -> str:
        # determine join type description
        if self.left and self.right: join_type = "LEFT or RIGHT JOIN"
        elif self.left: join_type = "LEFT JOIN"
        elif self.right: join_type = "RIGHT JOIN"
        else:  join_type = "JOIN"

        if self.max < 0:  return f'Must have minimum {self.min} {join_type}'
        elif self.min == self.max:  return f'Must have exactly {self.min} {join_type}'
        else: return f'Must have between {self.min} and {self.max} {join_type}'
