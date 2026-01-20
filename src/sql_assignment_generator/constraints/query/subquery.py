from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from ..costraintType import WhereConstraintType, DistinctOrUKInSelectConstraintType, AggregationConstraintType


class HasSubQueryConstraint(QueryConstraint):
    '''Requires the presence of a subquery in the SQL query. Function take in input min_tables and max_tables to specify number of subqueries required,
    state = True -> must have subquery or state = False -> must NOT have subquery and type to specify NESTED or NOT NESTED subquery.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, state: bool = True, typeNested: bool = True) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1
        
        self.state = state
        self.typeNested = typeNested


    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        #function helper to compute depth of SELECT
        # Depth 1 = main query
        # Depth 2 = simple subquery (NOT NESTED)
        # Depth 3 or more = nested subquery
        def get_max_select_depth(node):
            if not isinstance(node, exp.Expression):
                return 0
            
            max_child_depth = 0
            for arg_value in node.args.values():
                if isinstance(arg_value, list):
                    for item in arg_value:
                        if isinstance(item, exp.Expression):
                            max_child_depth = max(max_child_depth, get_max_select_depth(item))
                elif isinstance(arg_value, exp.Expression):
                    max_child_depth = max(max_child_depth, get_max_select_depth(arg_value))
            
            if isinstance(node, exp.Select):
                return 1 + max_child_depth
            
            return max_child_depth

        #compute total number of SELECT except main query 
        all_selects = list(query_ast.find_all(exp.Select))
        total_selects = len(all_selects)
        subquery_count = max(0, total_selects - 1)

        #compute depth
        max_depth = get_max_select_depth(query_ast)

        if not self.state: #state False (NO SUBQUERY)
            return subquery_count == 0

        #state True
        count_valid = False
        if self.max_tables > 0: count_valid = (self.min_tables <= subquery_count <= self.max_tables)
        else: count_valid = (self.min_tables <= subquery_count)
        
        if not count_valid:
            return False

        #type (NESTED / NON NESTED)
        if not self.typeNested: #"NOT NESTED": subquery exist Depth = 2 but not Depth < 3
            return max_depth == 2
        else: return True
    
    @property
    def description(self) -> str:
        if not self.state:
            return "Must have NO SUB-QUERY."

        if self.max_tables < 0: qty_desc = f"minimum {self.min_tables}"
        elif self.min_tables == self.max_tables: qty_desc = f"exactly {self.min_tables}"
        else: qty_desc = f"between {self.min_tables} and {self.max_tables}"

        if self.typeNested: type_desc = "SUB-QUERY"
        elif not self.typeNested: type_desc = "NOT NESTED SUB-QUERY"

        return f"Must have {qty_desc} {type_desc}"
