from collections import Counter
from .base import BaseConstraint
from sqlglot import Expression, exp
     
class HasAggregationConstraint(BaseConstraint):
    '''Requires the presence (or absence) of an aggregation function in the SQL query. 
    It is possible chose the type of aggregation function present in solution.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, type: list[str] = [], state: bool = True) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1

        self.type = type if type is not None else []
        self.state = state

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        type_map = {
            "SUM": exp.Sum,
            "AVG": exp.Avg,
            "COUNT": exp.Count,
            "MAX": exp.Max,
            "MIN": exp.Min,
            "EXTRACT": exp.Extract
        }

        #if type is empty consider all aggregation functions
        if not self.type: target_types = tuple(type_map.values())
        else: #if type has value take only sqlglot needed
            target_types = tuple(
                type_map[t.upper()] for t in self.type 
                if t.upper() in type_map
            )

            if not target_types:
                target_types = (exp.AggExp)

        # find_all(tuple) find all occurence in query and subquery
        aggregations_found = list(query_ast.find_all(target_types))
        count = len(aggregations_found)

        if not self.state: #case must NOT have AGGREGATION
            return count == 0
        else: #case must have AGGREGATION
            return self.min_tables <= count <= self.max_tables if self.max_tables > 0 else self.min_tables <= count
    
    @property
    def description(self) -> str:
        type_suffix = ""
        if self.type:
            joined_types = " or ".join(t.upper() for t in self.type)
            type_suffix = f"of type {joined_types}"
        if self.state == False: return "Must NOT have AGGREGATION."
        if (self.min_tables > self.max_tables): return f'Must have minimum {self.min_tables} AGGREGATION {type_suffix}' 
        elif (self.min_tables == self.max_tables): return f'Must have exactly {self.min_tables} AGGREGATION {type_suffix}'
        else: return f'Must have between {self.min_tables} and {self.max_tables} AGGREGATION {type_suffix}'

class HasSubQueryConstraint(BaseConstraint):
    '''Requires the presence of a subquery in the SQL query. Function take in input min_tables and max_tables to specify number of subqueries required,
    state = True -> must have subquery or state = False -> must NOT have subquery and type to specify NESTED or NOT NESTED subquery.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, state: bool = True, type: str = "") -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1
        
        self.state = state
        valid_types = ["", "NON NESTED"] 
        if type not in valid_types: raise ValueError(f"type must be one of {valid_types}")
        else: self.type = type


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
        if self.type == "NOT NESTED": #"NOT NESTED": subquery exist Depth = 2 but not Depth < 3
            return max_depth == 2
        else: return True
    
    @property
    def description(self) -> str:
        if not self.state:
            return "Must have NO SUB-QUERY."

        if self.max_tables < 0: qty_desc = f"minimum {self.min_tables}"
        elif self.min_tables == self.max_tables: qty_desc = f"exactly {self.min_tables}"
        else: qty_desc = f"between {self.min_tables} and {self.max_tables}"
        
        type_desc = "SUB-QUERY"
        if self.type == "": type_desc = "SUB-QUERY"
        elif self.type == "NOT NESTED": type_desc = "NOT NESTED SUB-QUERY"

        return f"Must have {qty_desc} {type_desc}."

class HasDistinctOrUniqueKeyInSelectConstraint(BaseConstraint):
    '''
    Checks for uniqueness constraints in the query.
    Can check for the DISTINCT keyword OR for the presence of Key columns in the SELECT clause.

    Args:
        min_tables: Min occurrences required.
        max_tables: Max occurrences required (-1 for no limit).
        state: If True, must be present. If False, must NOT be present.
        type: 
            - "DISTINCT": Checks for DISTINCT keyword.
            - "PK": Checks for Primary Keys in SELECT.
            - "UK": Checks for Primary OR Unique Keys in SELECT.
            - "DISTINCT/UK": Checks for DISTINCT keyword OR Primary/Unique Keys in SELECT.
    '''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, state: bool = True, type: str = "DISTINCT") -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1
        
        self.state = state
        valid_types = ["DISTINCT", "PK", "UK", "DISTINCT/UK"]
        if type not in valid_types: raise ValueError(f"type must be one of {valid_types}")
        self.type = type

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        distinct_count = 0
        key_count = 0

        #DISTINCT case
        if self.type in ["DISTINCT", "DISTINCT/UK"]:
            distinct_nodes = list(query_ast.find_all(exp.Distinct))
            distinct_count = len(distinct_nodes)

        #PK/UK case
        if self.type in ["PK", "UK", "DISTINCT/UK"]:
            #identify primary keys and unique keys from tables
            pks = set()
            uks = set()

            for table in tables:
                schema = table.this
                if not isinstance(schema, exp.Schema): continue
                
                #controll all column definitions to find inline PK/UK
                for col_def in schema.find_all(exp.ColumnDef):
                    col_name = col_def.this.output_name.lower()
                    for inline_constraint in col_def.args.get('constraints', []): 
                        if isinstance(inline_constraint.kind, exp.PrimaryKeyColumnConstraint): pks.add(col_name)
                        elif isinstance(inline_constraint.kind, exp.UniqueColumnConstraint): uks.add(col_name)

                #controll definition of Pk/UK at the end of CREATE TABLE (e.g. PRIMARY KEY (col1, col2))
                for constraint in schema.expressions:
                    if isinstance(constraint, exp.PrimaryKey):
                        for col in constraint.expressions:
                            pks.add(col.output_name.lower())
                    elif isinstance(constraint, exp.Constraint):
                        if isinstance(constraint.kind, exp.UniqueColumnConstraint):
                            if constraint.this:
                                cols = constraint.this.expressions if hasattr(constraint.this, 'expressions') else [constraint.this]
                                for col in cols:
                                    if isinstance(col, exp.Column):
                                        uks.add(col.output_name.lower())
                                    elif isinstance(col, exp.Identifier):
                                        uks.add(col.this.lower())

            if self.type == "PK": valid_keys = pks #only PK
            else: valid_keys = pks.union(uks) #UK or DISTINCT/UK: accept PK and UK

            #analyze SELECT clause to count how many valid keys are selected
            for select_node in query_ast.find_all(exp.Select):
                for expression in select_node.expressions:
                    found_cols = []
                    if isinstance(expression, exp.Column):
                        found_cols.append(expression.output_name.lower())
                    #case alias controll principal column (es: col AS alias)
                    elif isinstance(expression, exp.Alias):
                        for col in expression.this.find_all(exp.Column):
                            found_cols.append(col.output_name.lower())
                    else:# Case functions or complex expressions(SELECT COUNT(id))
                        for col in expression.find_all(exp.Column):
                            found_cols.append(col.output_name.lower())
                    for col_name in found_cols:
                        if col_name in valid_keys:
                            key_count += 1
                            break
        
        #final count based on type
        if self.type == "DISTINCT":
            final_count = distinct_count
        elif self.type in ["PK", "UK"]:
            final_count = key_count
        else: # DISTINCT/UK - or DISTINCT or KEY
            final_count = distinct_count + key_count

        if not self.state: return final_count == 0
        else: return final_count >= self.min_tables  if self.max_tables < 0 else self.min_tables <= final_count <= self.max_tables
    
    @property
    def description(self) -> str:
        if self.type == "DISTINCT": elem_name = "DISTINCT"
        elif self.type == "PK": elem_name = "PRIMARY KEY in SELECT"
        elif self.type == "UK": elem_name = "PRIMARY or UNIQUE KEY in SELECT"
        else: elem_name = "DISTINCT or PRIMARY/UNIQUE KEY in SELECT"
        
        if not self.state: return f"Must NOT have {elem_name}."
        
        if self.max_tables < 0: return f'Must have minimum {self.min_tables} {elem_name}.'
        elif self.min_tables == self.max_tables: return f'Must have exactly {self.min_tables} {elem_name}.'
        else: return f'Must have between {self.min_tables} and {self.max_tables} {elem_name}.'

# class HasDistinctConstraint(BaseConstraint):
#     '''Requires the presence (or absence) of the DISTINCT keyword.'''

#     def __init__(self, min_tables: int = 1, max_tables: int = -1, state: bool = True) -> None:
#         self.min_tables = min_tables
#         self.max_tables = max_tables if max_tables > min_tables else -1
#         self.state = state

#     def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
#         #look for all DISTINCT node in query
#         distinct_nodes = list(query_ast.find_all(exp.Distinct))
#         count = len(distinct_nodes)

#         if not self.state: #case: Must NOT have DISTINCT
#             return count == 0
#         else: #case: Must have DISTINCT
#             return count >= self.min_tables if self.max_tables < 0 else self.min_tables <= count <= self.max_tables
    
#     @property
#     def description(self) -> str:
#         if self.state == False: return "Must NOT have DISTINCT."
#         if self.max_tables < 0: return f'Must have minimum {self.min_tables} DISTINCT.'
#         elif self.min_tables == self.max_tables: return f'Must have exactly {self.min_tables} DISTINCT.'
#         else: return f'Must have between {self.min_tables} and {self.max_tables} DISTINCT.'
    
class HasGroupByConstraint(BaseConstraint):
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
            return "Must NOT have GROUP BY."
        
        if self.max_tables < 0: return f'Must have minimum {self.min_tables} GROUP BY.'
        elif self.min_tables == self.max_tables: return f'Must have exactly {self.min_tables} GROUP BY.'
        else: return f'Must have between {self.min_tables} and {self.max_tables} GROUP BY.'

class HasJoinConstraint(BaseConstraint):
    '''T'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1


    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        return True
    
    @property
    def description(self) -> str:
        if self.min_tables == self.max_tables:
            return f'Must have minimum {self.min_tables} .'
        else:
            return f'Must have between {self.min_tables} and {self.max_tables} .'

class HasOrderByConstraint(BaseConstraint):
    '''Requires the presence (or absence) of an ORDER BY clause.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, state: bool = True) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1
        
        self.state = state

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        #look for alla node ORDER BY in query
        order_nodes = list(query_ast.find_all(exp.Order))
        count = len(order_nodes)

        if not self.state: #case: Must NOT have ORDER BY
            return count == 0
        else: #case: Must have ORDER BY
            return count >= self.min_tables if self.max_tables == -1 else self.min_tables <= count <= self.max_tables
    
    @property
    def description(self) -> str:
        if self.state == False:
            return "Must NOT have ORDER BY."
        
        if self.max_tables < 0: return f'Must have minimum {self.min_tables} ORDER BY.'
        elif self.min_tables == self.max_tables: return f'Must have exactly {self.min_tables} ORDER BY.'
        else: return f'Must have between {self.min_tables} and {self.max_tables} ORDER BY.'

class HasUnionOrUnionAllConstraint(BaseConstraint):
    '''T'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        return True
    
    @property
    def description(self) -> str:
        if self.min_tables == self.max_tables:
            return f'Must have minimum {self.min_tables} .'
        else:
            return f'Must have between {self.min_tables} and {self.max_tables} .'

class HasWhereConstraint(BaseConstraint):
    '''Requires the presence of a WHERE clause in the SQL query with its specific characteristics.
    Function take in input: min_tables and max_tables to specify number of WHERE conditions required,
    type to specify the type of WHERE conditions required.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, type: str = "CLASSIC") -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1

        valid_types = ["CLASSIC", "STRING", "NULL/EMPTY", "MULTIPLE", "NESTED", "WILDCARD", "NO WILDCARD", "EXIST", 
                       "NOT EXIST", "EXIST/IN", "NOT", "COMPARISON OPERATORS", "ANY/ALL/IN", "HAVING"]
        
        if type not in valid_types: raise ValueError(f"type must be one of {valid_types}")
        else: self.type = type

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        if self.type == "CLASSIC": 
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
        elif self.type == "STRING": 
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
        elif self.type == "NULL/EMPTY": 
            count = 0
            where_nodes = list(query_ast.find_all(exp.Where)) #look for in all Where clausole

            for where_node in where_nodes:
                #look for string (col = '' or col <> '')
                for node in where_node.find_all(exp.EQ, exp.NEQ):
                    right_side = node.expression
                    #controll if it is a literal and if it is an empty string
                    if isinstance(right_side, exp.Literal) and right_side.is_string and right_side.this == "":
                        count += 1

                #look for IS NULL or IS NOT NULL
                for node in where_node.find_all(exp.Is):
                    if isinstance(node.expression, exp.Null):
                        count += 1

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        elif self.type == "MULTIPLE":
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
        elif self.type == "WILDCARD":
            count = 0
            wildcard_symbols = ['%', '_', '[', ']', '^', '-', '*', '+', '?', '(', ')', '{', '}']
            #look for LIKE clause
            for node in query_ast.find_all(exp.Like): 
                pattern = node.expression
                
                #take right part (node.expression) and controll if it is a string and if contains wildcard symbols
                if isinstance(pattern, exp.Literal) and pattern.is_string:
                    pattern_text = pattern.this
                    if any(symbol in pattern_text for symbol in wildcard_symbols):
                        count += 1

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        elif self.type == "NO WILDCARD":
            #if there is a LIKE return False
            if any(query_ast.find_all(exp.Like)):
                return False
            return True
        elif self.type == "ANY/ALL/IN":
            count = 0
            where_nodes = list(query_ast.find_all(exp.Where))

            for where_node in where_nodes:
                #look for ANY, ALL, IN
                target_types = (exp.In, exp.Any, exp.All)
                found_nodes = list(where_node.find_all(target_types))
                count += len(found_nodes)

            if self.max_tables < 0: return self.min_tables <= count
            return self.min_tables <= count <= self.max_tables
        elif self.type == "NESTED": return True
        elif self.type == "EXIST": return True
        elif self.type == "NOT EXIST": return True
        elif self.type == "EXIST/IN": return True
        elif self.type == "NOT": return True
        elif self.type == "COMPARISON OPERATORS": return True
        elif self.type == "HAVING": return True
        else: return False
    
    @property
    def description(self) -> str:
        type_descriptions = {
            "CLASSIC": "WHERE conditions",
            "STRING": "WHERE STRING conditions",
            "NULL/EMPTY": "WHERE NULL or EMPTY conditions",
            "MULTIPLE": "MULTIPLE WHERE conditions",
            "NESTED": "NESTED WHERE conditions",
            "WILDCARD": "WHERE conditions with WILDCARD",
            "NO WILDCARD": "WHERE conditions without WILDCARD",
            "EXIST": "EXIST in WHERE conditions",
            "NOT EXIST": "NOT EXIST in WHERE conditions",
            "EXIST/IN": "EXIST or IN in WHERE conditions",
            "NOT": "NOT in WHERE conditions",
            "COMPARISON OPERATORS": "COMPARISON OPERATORS in WHERE conditions",
            "ANY/ALL/IN": "ANY or ALL or IN in WHERE conditions",
            "HAVING": "WHERE or HAVING conditions",
        }

        suffix = type_descriptions.get(self.type, "WHERE conditions")
        if (self.min_tables > self.max_tables): count_str =  f"minimum {self.min_tables}" 
        elif (self.min_tables == self.max_tables): count_str = f"exactly {self.min_tables}"
        else: count_str = f"between {self.min_tables} and {self.max_tables}"
        return f"Must have {count_str} {suffix}."
