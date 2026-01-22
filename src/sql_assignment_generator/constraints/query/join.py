from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp

class NoJoin(QueryConstraint):
    '''
    Requires the ABSENCE of any JOIN clause in the SQL query.
    '''

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # check if there are any JOIN clauses in the query AST
        return not any(query_ast.find_all(exp.Join))
    
    @property
    def description(self) -> str:
        return "Must NOT have JOIN clause"
    

class RequireJoin(QueryConstraint):
    '''
    Requires the presence of JOINs.
    Can specify if strictly LEFT, RIGHT, or generic JOINs are required.
    '''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, left: bool = False, right: bool = False) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables >= min_tables else -1
        self.left = left
        self.right = right

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
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

        if self.max_tables < 0:
            return count >= self.min_tables
        return self.min_tables <= count <= self.max_tables
    
    @property
    def description(self) -> str:
        # determine join type description
        if self.left and self.right: join_type = "LEFT or RIGHT JOIN"
        elif self.left: join_type = "LEFT JOIN"
        elif self.right: join_type = "RIGHT JOIN"
        else:  join_type = "JOIN"

        if self.max_tables < 0:  return f'Must have minimum {self.min_tables} {join_type}'
        elif self.min_tables == self.max_tables:  return f'Must have exactly {self.min_tables} {join_type}'
        else: return f'Must have between {self.min_tables} and {self.max_tables} {join_type}'
