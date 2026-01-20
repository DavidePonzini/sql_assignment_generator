from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from ..costraintType import WhereConstraintType
from .base import QueryConstraint
from sqlglot import Expression, exp
from ..costraintType import WhereConstraintType
from collections import Counter


class HasWhereConstraint(QueryConstraint):
    '''Requires the presence of a WHERE clause in the SQL query with its specific characteristics.
    Function take in input: min_tables and max_tables to specify number of WHERE conditions required,
    type to specify the type of WHERE conditions required.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, type:  WhereConstraintType = WhereConstraintType.CLASSIC) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables >= min_tables else -1

        if type not in list(WhereConstraintType): raise ValueError(f"type must be one of {list(WhereConstraintType)}")
        else: self.type = type

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        if self.type == WhereConstraintType.CLASSIC: 
            #find all Where clausole 
            where_nodes = list(query_ast.find_all(exp.Where))
            total_conditions = 0
            
            #count conditions in each Where clause
            for where_node in where_nodes:
                current_count = 1
                current_count += len(list(where_node.find_all(exp.And)))
                current_count += len(list(where_node.find_all(exp.Or)))
                
                total_conditions += current_count
            if self.max_tables < 0: return self.min_tables <= total_conditions
            return self.min_tables <= total_conditions <= self.max_tables 
        elif self.type == WhereConstraintType.STRING: 
            count = 0
            where_nodes = list(query_ast.find_all(exp.Where)) #look for all Where clausole

            for where_node in where_nodes:
                comparison_types = (exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE, exp.LTE, exp.Like, exp.ILike) #look for comparison functions
                
                for node in where_node.find_all(comparison_types):
                    right_side = node.expression
                    
                    #controll if type is string literal
                    if isinstance(right_side, exp.Literal) and right_side.is_string: count += 1

                #count also IN with string list
                for node in where_node.find_all(exp.In):
                    values = node.args.get('expressions')
                    if values and isinstance(values, list):
                        has_string = any(
                            isinstance(v, exp.Literal) and v.is_string 
                            for v in values
                        )

                        if has_string: count += len(values)

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables 
        elif self.type == WhereConstraintType.EMPTY: 
            count = 0
            where_nodes = list(query_ast.find_all(exp.Where))

            for where_node in where_nodes:
                # look for empty string (col = '' or col <> '')
                for node in where_node.find_all(exp.EQ, exp.NEQ):
                    right_side = node.expression
                    # Ccontroll if string literal is empty
                    if isinstance(right_side, exp.Literal) and right_side.is_string and right_side.this == "":
                        count += 1

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables 
        elif self.type == WhereConstraintType.NULL: 
            count = 0
            where_nodes = list(query_ast.find_all(exp.Where))

            for where_node in where_nodes:
                # look for IS NULL and IS NOT NULL
                for node in where_node.find_all(exp.Is):
                    if isinstance(node.expression, exp.Null):
                        # if parent isn't NOT
                        if not isinstance(node.parent, exp.Not):
                            count += 1

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        elif self.type == WhereConstraintType.NOT_NULL: 
            count = 0
            where_nodes = list(query_ast.find_all(exp.Where))

            for where_node in where_nodes:
                # look for IS NULL and IS NOT NULL
                for node in where_node.find_all(exp.Is):
                    if isinstance(node.expression, exp.Null):
                        # if parent is NOT
                        if isinstance(node.parent, exp.Not):
                            count += 1

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        elif self.type == WhereConstraintType.MULTIPLE:
            #if i have (A OR B) AND C AND (D OR E) return 3 element: [A OR B, C, D OR E]
            def get_and_chunks(node):
                if isinstance(node, exp.And):
                    yield from get_and_chunks(node.this)
                    yield from get_and_chunks(node.expression)
                else:
                    yield node

            where_nodes = list(query_ast.find_all(exp.Where))
            total_multiple_conditions = 0
            for where_node in where_nodes:
                root_expr = where_node.this
                
                #all block divide by AND
                chunks = list(get_and_chunks(root_expr))
                for chunk in chunks:
                    #count occurrences of each left column in this block
                    col_counter = Counter()
                    comparison_types = (
                        exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE, exp.LTE, 
                        exp.Like, exp.ILike, exp.In, exp.Between
                    )

                    for comp in chunk.find_all(comparison_types):
                        lhs = comp.this
                        #extract all columns in the left side of the comparison also function (LOWER(col) = val)
                        for col in lhs.find_all(exp.Column):
                            col_counter[col.name] += 1

                    #if column appear >= 2 confronti we found multiple condition (es. col='A' OR col='B')
                    if any(c >= 2 for c in col_counter.values()):
                        total_multiple_conditions += 1

            if self.max_tables < 0: return self.min_tables <= total_multiple_conditions
            else: return self.min_tables <= total_multiple_conditions <= self.max_tables
        elif self.type == WhereConstraintType.WILDCARD:
            count = 0
            wildcard_symbols = ['%', '_', '[', ']', '^', '-', '*', '+', '?', '(', ')', '{', '}']
            
            # look for LIKE clause
            for node in query_ast.find_all(exp.Like): 
                pattern = node.expression
                
                # take right part and control if it is a string
                if isinstance(pattern, exp.Literal) and pattern.is_string:
                    pattern_text = pattern.this
                    
                    # Check if contains ANY wildcard symbol
                    has_wildcard = any(symbol in pattern_text for symbol in wildcard_symbols)
                    
                    # Check "real" letters count (at least 4) count characters that are NOT in the wildcard_symbols list
                    real_char_count = sum(1 for char in pattern_text if char not in wildcard_symbols)

                    # Both conditions must be true
                    if has_wildcard and real_char_count >= 4:
                        count += 1

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        elif self.type == WhereConstraintType.NO_WILDCARD:
            #if there is a LIKE return False
            if any(query_ast.find_all(exp.Like)):
                return False
            return True
        elif self.type == WhereConstraintType.NOT: 
            count = 0
            #look for where clausole
            where_nodes = list(query_ast.find_all(exp.Where))

            for where_node in where_nodes:
                #take all not nodes
                not_nodes = list(where_node.find_all(exp.Not))
                count += len(not_nodes)
            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        elif self.type == WhereConstraintType.NOT_EXIST:
            count = 0
            where_nodes = list(query_ast.find_all(exp.Where))

            for where_node in where_nodes:
                for not_node in where_node.find_all(exp.Not):
                    if isinstance(not_node.this, exp.Exists):
                        count += 1
            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables            
        elif self.type == WhereConstraintType.EXIST_OR_IN:
            pos_count = 0 #count: IN, EXISTS
            neg_count = 0 #count: NOT IN, NOT EXISTS
            
            where_nodes = list(query_ast.find_all(exp.Where))

            for where_node in where_nodes:
                #look for IN and EXISTS nodes and NOT version
                for node in where_node.find_all(exp.In, exp.Exists):
                    if isinstance(node.parent, exp.Not):
                        neg_count += 1
                    else:
                        pos_count += 1

            if pos_count < self.min_tables or neg_count < self.min_tables: return False
            if self.max_tables > 0: 
                if (pos_count + neg_count) > self.max_tables: return False
            return True       
        elif self.type == WhereConstraintType.COMPARISON_OPERATORS:
            count = 0
            target_operators = (
                exp.EQ,   # =
                exp.NEQ,  # <> o !=
                exp.GT,   # >
                exp.LT,   # <
                exp.GTE,  # >=
                exp.LTE,  # <=
                exp.Add,  # +
                exp.Sub,  # -
                exp.Mul,  # *
                exp.Div,  # /
                exp.Mod   # %
            )

            for where_node in query_ast.find_all(exp.Where):
                found_ops = list(where_node.find_all(target_operators))
                count += len(found_ops)

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        elif self.type == WhereConstraintType.NESTED:
            count = 0
            where_nodes = list(query_ast.find_all(exp.Where))
            for where_node in where_nodes:
                #look for parentesis (exp.Paren)
                for paren in where_node.find_all(exp.Paren):
                    #look for (cond1 OR/AND cond2).
                    if isinstance(paren.this, (exp.And, exp.Or)):
                        count += 1
                        
            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        elif self.type == WhereConstraintType.HAVING:
            count = 0
            has_where = False
            has_having = False

            #controll WHERE clause
            where_nodes = list(query_ast.find_all(exp.Where))
            if where_nodes:
                has_where = True
                for node in where_nodes:
                    count += 1
                    count += len(list(node.find_all(exp.And)))
                    count += len(list(node.find_all(exp.Or)))

            #controll HAVING clause
            having_nodes = list(query_ast.find_all(exp.Having))
            if having_nodes:
                has_having = True
                for node in having_nodes:
                    count += 1
                    count += len(list(node.find_all(exp.And)))
                    count += len(list(node.find_all(exp.Or)))

            #controll at least one of the two exists
            if not (has_where or has_having):
                return False

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        elif self.type == WhereConstraintType.EXIST:
            count = 0
            where_nodes = list(query_ast.find_all(exp.Where))

            for where_node in where_nodes:
                #look for all node EXIST (also NOT EXISTS)
                for exists_node in where_node.find_all(exp.Exists):
                    #if parent is NOT skip
                    if not isinstance(exists_node.parent, exp.Not):
                        count += 1

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        else: return False
    
    @property
    def description(self) -> str:
        suffix = self.type.value
        if (self.min_tables > self.max_tables): count_str =  f"minimum {self.min_tables}" 
        elif (self.min_tables == self.max_tables): count_str = f"exactly {self.min_tables}"
        else: count_str = f"between {self.min_tables} and {self.max_tables}"
        return f"Must have {count_str} {suffix}. It is mandatory that PK does NOT have comparison operator with a NUMBER"