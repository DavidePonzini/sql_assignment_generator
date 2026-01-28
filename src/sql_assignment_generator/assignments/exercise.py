from dataclasses import dataclass
from sql_error_taxonomy import SqlErrors
from sqlscope import Query

from ..constraints import QueryConstraint
from ..difficulty_level import DifficultyLevel
from .dataset import Dataset
from .. import llm
import dav_tools
from ..exceptions import ExerciseGenerationError, SQLParsingError


@dataclass
class Exercise:
    '''A SQL exercise consisting of a title, request, and solutions.'''

    title: str
    '''The title of the exercise.'''

    request: str
    '''The natural language request or question for the exercise.'''

    solutions: list[Query]
    '''The list of SQL query solutions for the exercise.'''

    difficulty: DifficultyLevel
    '''The difficulty level of the exercise.'''

    error: SqlErrors
    '''The SQL error type associated with the exercise.'''

    @staticmethod
    def generate(
        error: SqlErrors,
        difficulty: DifficultyLevel,
        constraints: list[QueryConstraint],
        extra_details: str,
        dataset: Dataset,
        title: str,
        *,
        max_attempts: int = 3,
    ) -> 'Exercise':
        '''Generate a SQL exercise based on the specified parameters.'''

        formatted_constraints = '\n'.join(f'- {constraint.description}' for constraint in constraints)

        if extra_details.strip():
            extra_details_formatted = f"The exercise must have the following characteristics:\n{extra_details}"
        else:
            extra_details_formatted = ""
        

        assignment_text =f'''
### CONTEXT (DATABASE SCHEMA AND DATA) ###
{dataset.to_sql_no_context()}

### GUIDELINES ###
Generate a SQL exercise based on the dataset above.
{extra_details_formatted}

### MANDATORY REQUIREMENTS FOR THE EXERCISE ###
{formatted_constraints}

#### JSON REQUIRED OUTPUT FORMAT ####
{{
    "request": "Extract and return ONLY NATURAL LANGUAGE query following the assigned constraints. NEVER ask to include mistake. Be concise and clear. Do NOT provide hints or explanations.",
    "solution": "Only a single and SYNTACTICALLY and SEMANTICALLY correct (executable with minimum 1 returned row) SQL query following the ASSIGNED CONSTRAINTS. The query must be well-formatted and match with request."
}}
'''
        messages = llm.Message()
        messages.add_message_user(assignment_text)

        for attempt in range(max_attempts):
            try:
                answer = llm.generate_answer(messages, json_format=llm.models.Assignment)
                assert isinstance(answer, llm.models.Assignment)
                
                #refinement of the natural language request to remove hints
                messages_refinement = llm.Message()
                refinement_prompt = (
                    f'''
For the following query solution:
--- SOLUTION START ---
{answer.solution}
--- SOLUTION END ---

Remove any kind of hints on how to write the query from its natural language request. 
Keep it simple and straighforward
Do not use generic phrases like "a certain amount"; instead specify exact terms.
Avoids mentioning tables explicitly
Removes any reference to joins or join keys
Keeps the condition purely at the problem level, not the SQL level.
Make it clear which columns should be selected. If any columns are aliased in the solution, make sure to reflect that in the request.
Do not use any formatting on the answer
The alias in select solution must be appear in natural language request.

Natural Language Request:
--- REQUEST START ---
{answer.request}
--- REQUEST END ---'''
                )

                messages_refinement.add_message_user(refinement_prompt)
                answer_refinement = llm.generate_answer(
                    messages_refinement,
                    json_format=llm.models.RemoveHints
                )

                assert isinstance(answer_refinement, llm.models.RemoveHints)
                dav_tools.messages.debug(f"Old Request: {answer.request}")
                dav_tools.messages.debug(f"Refined Request: {answer_refinement.request_without_hints}")
                answer.request = answer_refinement.request_without_hints

                # check syntax correctness of solution
                try:
                    query = Query(answer.solution, catalog=dataset.catalog)
                except Exception as e:
                    raise SQLParsingError(f"Generated SQL solution contains syntax errors: {e}", answer.solution)

                # constraint validation
                constraint_errors = []
                
                for constraint in constraints:
                    if not constraint.validate(query):
                        constraint_errors.append(constraint.description)

                if not constraint_errors:
                    dav_tools.messages.success(f"Exercise '{title}' generated and validated successfully.")
                    
                    return Exercise(
                        title=title,
                        request=answer.request,
                        solutions=[query],
                        difficulty=difficulty,
                        error=error
                    )

                # validation fail management
                dav_tools.messages.error(f'Validation failed for attempt {attempt + 1} (error: {error.name}). Missing requirements: {", ".join(constraint_errors)}')
                
                feedback = (
                    f'The previously generated solution was REJECTED because it missed the following requirements: {", ".join(constraint_errors)}. '
                    f'Please regenerate the JSON. The SQL solution MUST satisfy ALL the original constraints:\n{formatted_constraints}'
                )
                messages.add_message_user(feedback)
            
            except Exception as e:
                dav_tools.messages.error(f"Error during exercise generation (Attempt {attempt + 1}): {e}")
                messages.add_message_user(f"An error occurred: {str(e)}. Please regenerate valid JSON/SQL.")

        raise ExerciseGenerationError(f'Failed to generate a valid exercise for {error.name} after {max_attempts} attempts.')