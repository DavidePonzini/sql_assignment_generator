import re

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


def _check_aggregation(schema: list[str], solution: str, constraint: str) -> bool:
    match = re.search(r'(\d+)', constraint)
    num_required = int(match.group(1)) if match else 1
    aggregations_found = re.findall(r'\b(SUM|AVG|COUNT|MAX|MIN)\b', solution.upper())
    return len(aggregations_found) >= num_required

def _check_subquery(schema: list[str], solution: str, constraint: str) -> bool:
    return solution.upper().count('SELECT') > 1

def _check_where(schema: list[str], solution: str, constraint: str) -> bool:
    match = re.search(r'(\d+)', constraint)
    num_required = int(match.group(1)) if match else 1
    where_clauses = solution.upper().count('WHERE')
    if where_clauses == 0:
        return num_required == 0
    logical_operators = len(re.findall(r'\b(AND|OR)\b', solution.upper()))
    conditions_found = where_clauses + logical_operators
    return conditions_found >= num_required

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
        content_match = re.search(r'\((.*)\)', create_statement, re.DOTALL)
        if not content_match:
            continue
        content = content_match.group(1).strip()
        
        lines = [line.strip() for line in content.split(',') if line.strip()]

        column_lines = [
            line for line in lines
            if not line.upper().startswith(('PRIMARY KEY', 'FOREIGN KEY', 'CONSTRAINT', 'CHECK'))
        ]
        column_count = len(column_lines)
        
        if not (min_required <= column_count <= max_required):
            return False
            
    return True




CONSTRAINT_CHECKERS = {
    "COLUMNS X TABLE": _check_columns,
    "TABLE": _check_tables,
    "AGGREGATION": _check_aggregation,
    "SUB-QUERY": _check_subquery,
    "WHERE": _check_where,
}