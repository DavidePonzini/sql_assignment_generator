from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from ..costraintType import WhereConstraintType, DistinctOrUKInSelectConstraintType, AggregationConstraintType


class HasUnionOrUnionAllConstraint(QueryConstraint):
    '''
    Requires the presence (or absence) of UNION or UNION ALL.
    Also enforces specific usage logic based on legacy rules:
    - If tables in the two parts are DIFFERENT -> Must use UNION ALL.
    - If tables in the two parts are the SAME -> Must use UNION (simple).
    '''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, state: bool = True) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1
        self.state = state

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        #look for all UNION nodes in query
        union_nodes = list(query_ast.find_all(exp.Union))
        count = len(union_nodes)

        if not self.state: #case Must have NO UNION
            return count == 0
        if self.max_tables < 0: #case Must have minimum UNION
            if count < self.min_tables: return False
        if not (self.min_tables <= count <= self.max_tables): return False

        for node in union_nodes:
            #controll if it is UNION ALL or UNION if kind == 'ALL' is UNION ALL
            is_union_all = (node.kind and node.kind.upper() == 'ALL')
            left_tables = set(t.this.output_name.upper() for t in node.this.find_all(exp.Table))
            right_tables = set(t.this.output_name.upper() for t in node.expression.find_all(exp.Table))

            are_tables_different = (left_tables != right_tables)
            if are_tables_different: #if table are different (es. A e B) we need UNION ALL
                if not is_union_all:
                    return False
            else: #if table are the same (es. A e A) we need simple UNION
                if is_union_all: return False
        return True
    
    @property
    def description(self) -> str:
        if not self.state:
            return "Must NOT have UNION or UNION ALL"
        
        if self.max_tables < 0: return f'Must have minimum {self.min_tables} UNION or UNION ALL'
        elif self.min_tables == self.max_tables: return f'Must have exactly {self.min_tables} UNION or UNION ALL'
        else: return f'Must have between {self.min_tables} and {self.max_tables} UNION or UNION ALL'
