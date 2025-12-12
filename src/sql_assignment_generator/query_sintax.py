import re
from collections import Counter
from typing import List


######################################################## all type of WHERE condition checkers
def _check_where_string(solution_upper, min_required, max_required) -> bool:
    count = 0
    string_pattern = r"\b\w+\.?\w*\b\s*(?:[=<>!]|NOT\s+LIKE|LIKE)\s*'[^']+'"
    count += len(re.findall(string_pattern, solution_upper))
    
    in_pattern = r'\b\w+\.?\w*\b\s*IN\s*\(([^)]+)\)'
    in_conditions = re.findall(in_pattern, solution_upper)
    for in_list in in_conditions:
        if "'" in in_list and 'SELECT' not in in_list:
            count += (in_list.count(',') + 1)
    return min_required <= count <= max_required

def _check_where_wildcards(solution_upper, min_required, max_required, has_wildcard) -> bool:
    if has_wildcard:
        wildcard_pattern = r"LIKE\s+'[^']*%[^']*'"
        count = len(re.findall(wildcard_pattern, solution_upper))
        return min_required <= count <= max_required
    else:
        any_like_pattern = r"\bLIKE\b"
        if re.search(any_like_pattern, solution_upper):
            return False
        operators = re.findall(r'\bWHERE\b|\bHAVING\b|\bAND\b|\bOR\b', solution_upper)
        count = len(operators)
        return min_required <= count <= max_required
    
def _check_where_multiple(solution_upper, min_required, max_required) -> bool:
    where_match = re.search(r'\bWHERE\b(.*?)(?=\bGROUP BY|\bORDER BY|\bLIMIT|$)', solution_upper, re.DOTALL | re.IGNORECASE)
    
    if not where_match:
        return min_required <= 0 <= max_required

    where_content = where_match.group(1)
    major_conditions = re.split(r'\s+AND\s+(?![^()]*\))', where_content.strip())
    
    total_multiple_conditions = 0
    column_pattern = r'(\b[A-Z0-9_]+\b(?:\.\b[A-Z0-9_]+\b)?)\s*(?:[=<>!]|>=|<=|\bNOT\s+LIKE\b|\bLIKE\b|\bIN\b)'

    for condition in major_conditions:
        columns_in_condition = re.findall(column_pattern, condition)
        if not columns_in_condition:
            continue

        column_counts = Counter(columns_in_condition)
        if any(count >= 2 for count in column_counts.values()):
            total_multiple_conditions += 1
            
    return min_required <= total_multiple_conditions <= max_required

def _check_where_in_any_all_exist(solution_upper, min_required, max_required, constraint_upper) -> bool:
    current_count = 0
    count_not_exists = len(re.findall(r'\bNOT\s+EXISTS\b', solution_upper)) #count NOT EXIST
    count_total_exists = len(re.findall(r'\bEXISTS\b', solution_upper)) #count EXISTS
    count_positive_exists = count_total_exists - count_not_exists

    # ---IN---
    if re.search(r'\bIN\b(?!\s+WHERE)', constraint_upper): current_count += len(re.findall(r'\bIN\b', solution_upper))
    # ---ANY---
    if 'ANY' in constraint_upper: current_count += len(re.findall(r'\bANY\b', solution_upper))
    # ---ALL---
    if 'ALL' in constraint_upper: current_count += len(re.findall(r'\bALL\b', solution_upper))
    # ---NOT EXIST---
    if 'NOT EXIST' in constraint_upper: current_count += count_not_exists #count NOT EXIST
    # ---EXIST---
    constraint_temp = constraint_upper.replace("NOT EXIST", "") #remove NOT EXIST
    if "EXIST" in constraint_temp: current_count += count_positive_exists #count EXIST

    return min_required <= current_count <= max_required

def _check_where_not(solution_upper, min_required, max_required) -> bool:
    #Found word "NOT".
    pattern = r'\bNOT\b'
    
    #Found corrispondence in query and count it
    matches = re.findall(pattern, solution_upper)
    count = len(matches)
    
    #Its correct number?
    return min_required <= count <= max_required

def _check_where_comparison(solution_upper, min_required, max_required) -> bool:
    where_match = re.search(r'\bWHERE\b(.*?)(?=\bGROUP BY|\bORDER BY|\bLIMIT|$)', solution_upper, re.DOTALL | re.IGNORECASE)
   
    if not where_match:
        return min_required <= 0 <= max_required

    where_content = where_match.group(1)
    where_content_clean = re.sub(r"'[^']*'", '', where_content)
    pattern = r'(>=|<=|<>|!=|=|>|<|\+|\-|\*|\/|%)'
    
    matches = re.findall(pattern, where_content_clean)
    count = len(matches)

    return min_required <= count <= max_required

def _check_where_nested(solution_upper, min_required, max_required) -> bool:
    #extract WHERE content
    where_match = re.search(r'\bWHERE\b(.*?)(?=\bGROUP BY|\bORDER BY|\bLIMIT|$)', solution_upper, re.DOTALL | re.IGNORECASE)
    
    if not where_match:
        return min_required <= 0 <= max_required

    where_content = where_match.group(1)
    where_content_clean = re.sub(r"'[^']*'", '', where_content)

    #sub-query cannot be counted as nested condition, remove it
    where_content_clean = re.sub(r'\(\s*SELECT.*?\)', '', where_content_clean, flags=re.DOTALL)

    #look for pattern as (condizione1 OR condizione2) or (condizione1 AND condizione2)
    pattern = r'\([^()]*\b(OR|AND)\b[^()]*\)'
    matches = re.findall(pattern, where_content_clean)
    count = len(matches)

    return min_required <= count <= max_required

def _check_where_having(solution_upper, min_required, max_required, constraint_upper) -> bool:
    # 1. Verifica presenza delle clausole nella soluzione
    has_where = bool(re.search(r'\bWHERE\b', solution_upper))
    has_having = bool(re.search(r'\bHAVING\b', solution_upper))

    #case AND both WHERE and HAVING must be present
    if 'AND' in constraint_upper:
        if not (has_where and has_having):
            return False
    #case OR at least one of WHERE or HAVING must be present
    elif 'OR' in constraint_upper:
        if not (has_where or has_having):
            return False

    #count how much condition we have in total (WHERE + HAVING + AND + OR)
    operators = re.findall(r'\bWHERE\b|\bHAVING\b|\bAND\b|\bOR\b', solution_upper)
    count = len(operators)

    return min_required <= count <= max_required


######################################################## suport functions
def _get_id_columns(schema: List[str]) -> set[str]:
    """
    Column that are defined as PRIMARY KEY or UNIQUE in the schema.
    """
    id_columns = set()
    
    # Pattern to find "PRIMARY KEY" or "UNIQUE"
    inline_pattern = re.compile(r'(\w+)\s+\w+\s+(?:PRIMARY\s+KEY|UNIQUE)', re.IGNORECASE)    
    constraint_pattern = re.compile(r'(?:PRIMARY\s+KEY|UNIQUE)\s*\((.*?)\)', re.IGNORECASE)

    for create_statement in schema:
        for match in inline_pattern.finditer(create_statement):
            id_columns.add(match.group(1).upper())
            
        for match in constraint_pattern.finditer(create_statement):
            columns_in_constraint = [col.strip() for col in match.group(1).split(',')]
            for col_name in columns_in_constraint:
                id_columns.add(col_name.upper())
                
    return id_columns

def _get_distinct_columns(solution: str) -> set[str]:
    """
    Column that are used with DISTINCT in the solution.
    """
    distinct_columns = set()
    
    # Pattern to found "DISTINCT col1, col2, ..."
    pattern = re.compile(r'DISTINCT\s+(.*?)\s+FROM', re.IGNORECASE | re.DOTALL)
    
    matches = pattern.findall(solution)
    for column_list_str in matches:
        column_list_str = re.sub(r'\w+\(.*?\)', '', column_list_str)
        
        columns = [col.strip() for col in column_list_str.split(',')]
        for col_name in columns:
            if col_name:
                actual_name = col_name.split('.')[-1]
                distinct_columns.add(actual_name.upper())
                
    return distinct_columns


######################################################## costraint checkers

def _check_where(schema: list[str], solution: str, constraint: str) -> bool:
    solution_upper = solution.upper()
    constraint_upper = constraint.upper()
    
    if "WHERE" in constraint_upper and "HAVING" not in constraint_upper:
        if 'WHERE' not in solution_upper:
            return False

    numbers = [int(n) for n in re.findall(r'\d+', constraint)]
    min_required = numbers[0] if numbers else 1
    max_required = numbers[1] if len(numbers) > 1 else float('inf')

    #all type of WHERE condition used
    if 'HAVING' in constraint_upper: return _check_where_having(solution_upper, min_required, max_required, constraint_upper)
    elif 'MULTIPLE' in constraint_upper: return _check_where_multiple(solution_upper, min_required, max_required)
    elif 'NESTED' in constraint_upper: return _check_where_nested(solution_upper, min_required, max_required)
    elif 'WITHOUT WILDCARDS' in constraint_upper: return _check_where_wildcards(solution_upper, min_required, max_required, False)
    elif 'WILDCARDS' in constraint_upper: return _check_where_wildcards(solution_upper, min_required, max_required, True)
    elif 'STRING' in constraint_upper: return _check_where_string(solution_upper, min_required, max_required)
    elif 'IN' in constraint_upper or 'ANY' in constraint_upper or 'ALL' in constraint_upper or 'EXIST' in constraint_upper: 
        return _check_where_in_any_all_exist(solution_upper, min_required, max_required, constraint_upper)
    elif 'NOT' in constraint_upper: return _check_where_not(solution_upper, min_required, max_required)
    elif 'COMPARISON OPERATOR' in constraint_upper: return _check_where_comparison(solution_upper, min_required, max_required)
    else:
        operators = re.findall(r'\bWHERE\b|\bHAVING\b|\bAND\b|\bOR\b', solution_upper)
        count = len(operators)
        if len(numbers) <= 1:
             max_required = float('inf')
        else:
             max_required = numbers[1]
        return min_required <= count <= max_required

def _check_tables(schema: list[str], solution: str, constraint: str) -> bool:
    if not schema:
        return False
    
    constraint_upper = constraint.upper()
    if 'CREATE TABLE' in constraint_upper:
        return True
    
    numbers = [int(n) for n in re.findall(r'\d+', constraint)] # extract number in constraint ( must have 2-6 CREATE TABLE -> [2,6])
    if not numbers:
        return True
    min_required = numbers[0]
    max_required = numbers[1] if len(numbers) > 1 else float('inf')  # if there are 2 number we have min and max, otherwise only min value

    tables_created = len(schema) #number of table
    
    if 'CHECK' in constraint_upper: #try to find if there is CHECK as ask in condition
        check_found = False
        for table_sql in schema: 
            if re.search(r'\bCHECK\b', table_sql, re.IGNORECASE):
                check_found = True
                break
        
        if not check_found:
            return False

    return min_required <= tables_created <= max_required #controll if it is valid number

def _check_columns(schema: list[str], solution: str, constraint: str) -> bool:
    if not schema:
        return False
    
    constraint_upper = constraint.upper()
    if 'COLUMNS' not in constraint_upper:
        return True
    
    numbers = [int(n) for n in re.findall(r'\d+', constraint)]
    if not numbers:
        return True
    min_required = numbers[0]
    max_required = numbers[1] if len(numbers) > 1 else float('inf')
    if not schema:
        return False
    
    for create_statement in schema:
        content_match = re.search(r'\((.*)\)', create_statement, re.DOTALL) #take element inside CREATE TABLE()
        if not content_match:
            continue
        content = content_match.group(1).strip() #extract string
        
        lines = [line.strip() for line in content.split(',') if line.strip()] #divide the element for ','

        #now we filter the list to count only the true column definitions
        column_lines = [
            line for line in lines
            if not line.upper().startswith(('PRIMARY KEY', 'FOREIGN KEY', 'CONSTRAINT', 'CHECK'))
        ]
        column_count = len(column_lines) #remaining elements are the column number
        
        if not (min_required <= column_count <= max_required): return False
    return True

def _check_aggregation(schema: list[str], solution: str, constraint: str) -> bool:
    #extract constraints number
    constraint_upper = constraint.upper()
    match = re.search(r'(\d+)', constraint) 
    num_required = int(match.group(1)) if match else 1
    possible_aggregations = ['SUM', 'AVG', 'COUNT', 'MAX', 'MIN', 'EXTRACT'] #all possible aggregation function that we can find

    #controll if there is NO AGGREGATION in constraint
    if 'NO AGGREGATION' in constraint_upper:
        search_pattern = fr'\b({"|".join(possible_aggregations)})\b'
        aggregations_found = re.findall(search_pattern, solution.upper())
        return len(aggregations_found) == 0
    
    #controll if there are function in constraint 
    specific_aggregations_in_constraint = [
        agg_func for agg_func in possible_aggregations 
        if agg_func in constraint.upper()
    ]

    #generic function, look for all type of aggregate function
    if not specific_aggregations_in_constraint:
        search_pattern_core = '|'.join(possible_aggregations)
    else:
        #specific function, look for only mention function
        search_pattern_core = '|'.join(specific_aggregations_in_constraint)
    search_pattern = fr'\b({search_pattern_core})\b'

    #look for all occurence of function
    aggregations_found = re.findall(search_pattern, solution.upper())
    return len(aggregations_found) >= num_required

def _check_subquery(schema: list[str], solution: str, constraint: str) -> bool:
    solution_upper = solution.upper()
    constraint_upper = constraint.upper()
    solution_clean = re.sub(r"'[^']*'", '', solution_upper)
    tokens = re.finditer(r'\(|\)|\bSELECT\b', solution_clean)
    
    current_depth = 0
    select_depths = []

    for match in tokens:
        token = match.group()
        if token == '(':
            current_depth += 1
        elif token == ')':
            current_depth -= 1
        elif token == 'SELECT':
            select_depths.append(current_depth)

    has_real_subquery = False
    max_nesting_level = 0

    if select_depths:
        base_depth = min(select_depths) 
        relative_depths = [d - base_depth for d in select_depths]
        subquery_depths = [d for d in relative_depths if d > 0]
        
        if subquery_depths:
            has_real_subquery = True
            max_nesting_level = max(subquery_depths)

    if 'NO SUB-QUERY' in constraint_upper: #case "must have NO SUB-QUERY"
        return not has_real_subquery
    if not has_real_subquery:
        return False
    if 'NOT NESTED' in constraint_upper: #case "must have SUB-QUERY NOT NESTED"
        return max_nesting_level == 1    
    elif 'NESTED' in constraint_upper: #case "must have SUB-QUERY NESTED"
        return max_nesting_level >= 2       
    else:   #case "must have SUB-QUERY"
        return True

def _check_distinct(schema: list[str], solution: str, constraint: str) -> bool:
    id_columns = _get_id_columns(schema)
    distinct_columns = _get_distinct_columns(solution)

    if id_columns.intersection(distinct_columns):
        return False
    
    #extract number of occurence
    numbers = [int(n) for n in re.findall(r'\d+', constraint)]
    min_required = numbers[0] if numbers else 1
    max_required = numbers[1] if len(numbers) > 1 else float('inf')

    #look for all distinct occurrence in solution
    solution_upper = solution.upper()
    pattern = r'\bDISTINCT\b'
    distincts_found = re.findall(pattern, solution_upper)
    
    #count occurence
    count = len(distincts_found)
    return min_required <= count <= max_required

def _check_join(schema: list[str], solution: str, constraint: str) -> bool:
    constraint_upper = constraint.upper()
    solution_upper = solution.upper()
    
    numbers = [int(n) for n in re.findall(r'\d+', constraint)]
    min_required = numbers[0] if numbers else 1
    max_required = numbers[1] if len(numbers) > 1 else float('inf')

    if 'LEFT' in constraint_upper and 'RIGHT' in constraint_upper:
        #look for LEFT JOIN, LEFT OUTER JOIN, RIGHT JOIN, RIGHT OUTER JOIN
        pattern = r'\b(LEFT|RIGHT)\s+(?:OUTER\s+)?JOIN\b'

    elif 'LEFT' in constraint_upper:
        #look for "LEFT JOIN" or "LEFT OUTER JOIN"
        pattern = r'\bLEFT\s+(?:OUTER\s+)?JOIN\b'
    
    elif 'RIGHT' in constraint_upper:
        #look for "RIGHT JOIN" or "RIGHT OUTER JOIN"
        pattern = r'\bRIGHT\s+(?:OUTER\s+)?JOIN\b'
        
    else:
        #look for "INNER JOIN"
        pattern = r'\bJOIN\b'

    matches = re.findall(pattern, solution_upper)
    count = len(matches)
    
    return min_required <= count <= max_required

def _check_order_by(schema: list[str], solution: str, constraint: str) -> bool:
    constraint_upper = constraint.upper()
    solution_upper = solution.upper()

    if 'NO ORDER BY' in constraint_upper:
        return len(re.findall(r'\bORDER\s+BY\b', solution_upper)) == 0

    numbers = [int(n) for n in re.findall(r'\d+', constraint)]
    min_columns = numbers[0] if numbers else 1
    max_columns = numbers[1] if len(numbers) > 1 else float('inf')

    pattern = r'\bORDER\s+BY\b(.*?)(?=\bLIMIT\b|\bOFFSET\b|$)'
    matches = re.findall(pattern, solution_upper, re.DOTALL)

    if len(matches) != 1:
        return False

    content = matches[0].strip()
    columns = [col.strip() for col in content.split(',') if col.strip()]
    column_count = len(columns)

    return min_columns <= column_count <= max_columns

def _check_group_by(schema: list[str], solution: str, constraint: str) -> bool:
    constraint_upper = constraint.upper()
    solution_upper = solution.upper()

    #case group by no necessary: "must have NO GROUP BY"
    if 'NO GROUP BY' in constraint_upper:
        return len(re.findall(r'\bGROUP\s+BY\b', solution_upper)) == 0

    numbers = [int(n) for n in re.findall(r'\d+', constraint)]
    min_columns = numbers[0] if numbers else 1
    max_columns = numbers[1] if len(numbers) > 1 else float('inf')

    pattern = r'\bGROUP\s+BY\b(.*?)(?=\bHAVING\b|\bORDER\s+BY\b|\bLIMIT\b|$)'
    matches = re.findall(pattern, solution_upper, re.DOTALL)

    if len(matches) != 1:
        return False

    content = matches[0].strip()
    columns = [col.strip() for col in content.split(',') if col.strip()]
    column_count = len(columns)

    return min_columns <= column_count <= max_columns

def _check_union(schema: list[str], solution: str, constraint: str) -> bool:
    constraint_upper = constraint.upper()
    solution_upper = solution.upper()

    #case: "must have NO UNION"
    if 'NO UNION' in constraint_upper:
        return len(re.findall(r'\bUNION\b', solution_upper)) == 0

    numbers = [int(n) for n in re.findall(r'\d+', constraint)]
    min_required = numbers[0] if numbers else 1
    max_required = numbers[1] if len(numbers) > 1 else float('inf')

    #count UNION occurrence
    pattern = r'\bUNION\b'
    matches = re.findall(pattern, solution_upper)
    count = len(matches)

    if not (min_required <= count <= max_required):
        return False

    has_union_all = bool(re.search(r'\bUNION\s+ALL\b', solution_upper))
    has_simple_union = bool(re.search(r'\bUNION\b(?!\s+ALL)', solution_upper)) # UNION senza ALL successivo

    if not has_union_all and not has_simple_union:
        return False

    if has_union_all:
        parts = re.split(r'\bUNION\s+ALL\b', solution_upper, maxsplit=1)
        used_operator_is_all = True
    else:
        parts = re.split(r'\bUNION\b', solution_upper, maxsplit=1)
        used_operator_is_all = False
    
    #division in two query
    if len(parts) < 2:
        return False

    query_part_1 = parts[0]
    query_part_2 = parts[1]

    #take FROM tables
    def extract_tables_from_part(sql_segment):
        return set(re.findall(r'(?:\bFROM|\bJOIN)\s+([A-Z0-9_]+)', sql_segment))

    tables_1 = extract_tables_from_part(query_part_1)
    tables_2 = extract_tables_from_part(query_part_2)

    are_tables_different = (tables_1 != tables_2)

    #if tables in the two part are different
    if are_tables_different:
        if not used_operator_is_all:
            return False
    #if tables in the two part are same
    else:
        if used_operator_is_all:
            return False

    return True

def _check_same_pk(schema: list[str], solution: str, constraint: str) -> bool:
    numbers = [int(n) for n in re.findall(r'\d+', constraint)]
    min_required = numbers[0] if numbers else 2

    pk_names = []

    for create_statement in schema:
        stmt = create_statement.upper().replace('\n', ' ')
        content_match = re.search(r'\((.*)\)', stmt, re.DOTALL)
        if not content_match:
            continue
        content = content_match.group(1)

        #found primary key
        pk_constraint_match = re.search(r'PRIMARY\s+KEY\s*\(\s*([A-Z0-9_]+)\s*\)', content)
        
        if pk_constraint_match:
            #found PK as PRIMARY KEY (id)
            pk_names.append(pk_constraint_match.group(1))
        else:
            #column as PRIMARY KEY
            lines = [line.strip() for line in content.split(',') if line.strip()]
            for line in lines:
                if 'PRIMARY KEY' in line and 'FOREIGN KEY' not in line and not line.startswith('PRIMARY KEY') and not line.startswith('CONSTRAINT'):
                    parts = line.split()
                    if parts:
                        pk_names.append(parts[0])
                        break

    #count primary key occurrence
    pk_counts = Counter(pk_names)
    return any(count >= min_required for count in pk_counts.values())


######################################################## main function
def is_solution_valid(schema: list[str], solution: str, constraints: list[str]) -> tuple[bool, list[str]]:
    """
    Function to verify if generated exercise (schema and solution) respect all costraints.
    """
    missing_constraints = []
    for constraint in constraints:
        for keyword, checker_func in CONSTRAINT_CHECKERS.items():
            if keyword in constraint.upper():
                if not checker_func(schema, solution, constraint):
                    missing_constraints.append(constraint)
                break
        
    return len(missing_constraints) == 0, list(set(missing_constraints))

CONSTRAINT_CHECKERS = {
    "SAME PK": _check_same_pk, 
    "TABLE": _check_tables,
    "COLUMNS PER TABLE": _check_columns,
    "WHERE": _check_where,
    "DISTINCT": _check_distinct,
    "AGGREGATION": _check_aggregation,
    "SUB-QUERY": _check_subquery,
    "JOIN": _check_join,
    "ORDER BY": _check_order_by,
    "GROUP BY": _check_group_by,
    "UNION": _check_union
}