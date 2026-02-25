from ...constraints import QueryConstraint
from sqlscope import Query

def prompt_generate(dataset_str: str, extra_details: str, constraints: list[QueryConstraint]) -> str:

    formatted_constraints = '\n'.join(f'- {constraint.description}' for constraint in constraints)

    if extra_details.strip():
        extra_details_formatted = f"The exercise must have the following characteristics:\n{extra_details}"
    else:
        extra_details_formatted = ""

    return f'''
### CONTEXT (DATABASE SCHEMA AND DATA) ###
{dataset_str}

### GUIDELINES ###
Generate a SQL exercise based on the dataset above.
{extra_details_formatted}

### MANDATORY REQUIREMENTS FOR THE EXERCISE ###
{formatted_constraints}

#### JSON REQUIRED OUTPUT FORMAT ####
{{
    "request": "Extract and return ONLY the natural language query request, following the specified constraints. Never ask to include mistakes. Be concise and clear. Do not provide hints or explanations.",
    "solution": "Only a single syntactically and semantically correct (i.e. executable with minimum 1 returned row) SQL query that solves the exercise."
}}
'''


def feedback_validation_errors(errors: list[str]) -> str:
    return (
        f"The previous JSON output was rejected because it violated these constraints: {', '.join(errors)}\n"
        "Regenerate the JSON to satisfy all constraints."
    )


def prompt_refine_request(request: str, query: Query) -> str:
    result = f'''For the following query solution:
--- SOLUTION START ---
{query.sql}
--- SOLUTION END ---

Reword the natural language request to remove any kind of hints on how to write it. 
Keep the condition purely at the problem level, not the SQL level.
Keep it realistic, simple and straightforward. It doesn't have to sound like a school exercise, but like a real-world request.
Do not use generic phrases like "a certain amount"; instead specify exact terms.
Avoid mentioning tables explicitly. Remove any reference to joins or join keys.
Do not use any formatting on the answer.
'''

    # Aliases
    result += 'Make it clear which columns should be selected. If any columns are aliased in the solution, make sure to reflect that in the request, otherwise students might be confused.'    
    aliases: list[tuple[str, str]] = []
    for col in query.main_query.output.columns:
        if col.name != col.real_name:
            aliases.append((col.real_name, col.name))

    if aliases:
        aliases_str = ', '.join([f'"{alias}"' for real_name, alias in aliases])
        result += f"\nIn particular, you must specify the need to use the following aliases: {aliases_str}."

    result += f'''

Natural Language Request:
--- REQUEST START ---
{request}
--- REQUEST END ---
'''
    
    return result