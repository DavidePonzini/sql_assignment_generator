import re
from collections import Counter

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

def _check_where_wildcards(solution_upper, min_required, max_required) -> bool:
    wildcard_pattern = r"LIKE\s+'[^']*%[^']*'"
    count = len(re.findall(wildcard_pattern, solution_upper))
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

def _check_where_in_any_all(solution_upper, min_required, max_required) -> bool:
    pattern = r'\b(IN|ANY|ALL)\b'
    
    matches = re.findall(pattern, solution_upper)
    count = len(matches)

    return min_required <= count <= max_required

def _check_where_not(solution_upper, min_required, max_required) -> bool:
    #Found word "NOT".
    pattern = r'\bNOT\b'
    
    #Found corrispondence in query and count it
    matches = re.findall(pattern, solution_upper)
    count = len(matches)
    
    #Its correct number?
    return min_required <= count <= max_required

def _check_where_exists(solution_upper, min_required, max_required, exist) -> bool:
    # look for word "EXISTS".
    if exist:
        pattern = r'\bEXISTS\b'
    else:
        pattern = r'\bNOT EXISTS\b'
    
    matches = re.findall(pattern, solution_upper)
    count = len(matches)
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


def _check_where(schema: list[str], solution: str, constraint: str) -> bool:
    solution_upper = solution.upper()
    
    if "WHERE" in constraint.upper() and 'WHERE' not in solution_upper:
        return False
    if 'WHERE' not in solution_upper:
        return True

    numbers = [int(n) for n in re.findall(r'\d+', constraint)]
    min_required = numbers[0] if numbers else 1
    max_required = numbers[1] if len(numbers) > 1 else float('inf')
    constraint_upper = constraint.upper()

    #all type of WHERE condition used
    if 'MULTIPLE' in constraint_upper: return _check_where_multiple(solution_upper, min_required, max_required)
    elif 'WILDCARDS' in constraint_upper: return _check_where_wildcards(solution_upper, min_required, max_required)
    elif 'STRING' in constraint_upper: return _check_where_string(solution_upper, min_required, max_required)
    elif 'NOT EXIST' in constraint_upper: return _check_where_exists(solution_upper, min_required, max_required, False)
    elif 'EXIST' in constraint_upper: return _check_where_exists(solution_upper, min_required, max_required, True)
    elif 'NOT' in constraint_upper: return _check_where_not(solution_upper, min_required, max_required)
    elif 'COMPARISON OPERATOR' in constraint_upper: return _check_where_comparison(solution_upper, min_required, max_required)
    elif 'IN' in constraint_upper or 'ANY' in constraint_upper or 'ALL' in constraint_upper: return _check_where_in_any_all(solution_upper, min_required, max_required)
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

def _check_aggregation(schema: list[str], solution: str, constraint: str) -> bool:
    #extract constraints number
    match = re.search(r'(\d+)', constraint) 
    num_required = int(match.group(1)) if match else 1

    possible_aggregations = ['SUM', 'AVG', 'COUNT', 'MAX', 'MIN'] #all possible aggregation function that we can find

    #controll if there are function in constraint 
    specific_aggregations_in_constraint = [
        agg_func for agg_func in possible_aggregations 
        if agg_func in constraint.upper()
    ]

    # --- 2. Costruzione Dinamica del Pattern di Ricerca ---
    
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
    return solution.upper().count('SELECT') > 1

def _check_distinct(schema: list[str], solution: str, constraint: str) -> bool:
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
    "TABLE": _check_tables,
    "COLUMNS X TABLE": _check_columns,
    "WHERE": _check_where,
    "DISTINCT": _check_distinct,
    "AGGREGATION": _check_aggregation,
    "SUB-QUERY": _check_subquery
}