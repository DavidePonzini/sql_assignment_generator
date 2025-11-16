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
    column_pattern = r'(\b[A-Z0-9_]+\b(?:\.\b[A-Z0-9_]+\b)?)\s*(?:[=<>!]|>=|<=|\bNOT\s+LIKE\b|\bLIKE\b|\bIN\b)'
    columns_used = re.findall(column_pattern, solution_upper)

    column_counts = Counter(columns_used)

    total_multiple_conditions = 0
    for column in column_counts:
        count = column_counts[column]
        total_multiple_conditions += count // 2
        
    return min_required <= total_multiple_conditions <= max_required
 



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



def _check_tables(schema: list[str], solution: str, constraint: str) -> bool:
    numbers = [int(n) for n in re.findall(r'\d+', constraint)] # extract number in constraint ( must have 2-6 CREATE TABLE -> [2,6])
    if not numbers:
        return True
    min_required = numbers[0]
    max_required = numbers[1] if len(numbers) > 1 else min_required  # if there are 2 number we have min and max, otherwise only min value

    tables_created = len(schema) #number of table
    
    return min_required <= tables_created <= max_required #controll if it is valid number

def _check_columns(schema: list[str], solution: str, constraint: str) -> bool:
    numbers = [int(n) for n in re.findall(r'\d+', constraint)]
    if not numbers:
        return True
    min_required = numbers[0]
    max_required = numbers[1] if len(numbers) > 1 else min_required
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

    if 'MULTIPLE' in constraint_upper: return _check_where_multiple(solution_upper, min_required, max_required)
    elif 'WILDCARDS' in constraint_upper: return _check_where_wildcards(solution_upper, min_required, max_required)
    elif 'STRING' in constraint_upper: return _check_where_string(solution_upper, min_required, max_required)
    else:
        operators = re.findall(r'\bWHERE\b|\bHAVING\b|\bAND\b|\bOR\b', solution_upper)
        count = len(operators)
        if len(numbers) <= 1:
             max_required = float('inf')
        else:
             max_required = numbers[1]
        return min_required <= count <= max_required


CONSTRAINT_CHECKERS = {
    "COLUMNS X TABLE": _check_columns,
    "TABLE": _check_tables,
    "WHERE": _check_where,
    "AGGREGATION": _check_aggregation,
    "SUB-QUERY": _check_subquery
}