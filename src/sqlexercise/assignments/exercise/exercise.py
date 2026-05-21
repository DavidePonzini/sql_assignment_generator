from dataclasses import dataclass
from sqlerrors import SqlErrors
from sqlscope import Query
import os
from typing import Callable
import logging

from . import strings
from ..dataset import Dataset
from ...constraints import QueryConstraint
from ...difficulty_level import DifficultyLevel
from ... import llm
from ...exceptions import ExerciseGenerationError, SQLParsingError, ConstraintValidationError
from ...translatable_text import TranslatableText
from ...db import get_database, QueryExecutionError

logger = logging.getLogger(__name__)

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
        *,
        db_host: str,
        db_port: int,
        db_user: str,
        db_password: str,
        extra_details: str,
        dataset: Dataset,
        title: str,
        sql_dialect: str,
        language: str,
        max_attempts: int = 3,
        on_attempt_start: Callable[[], None] = lambda: None,
    ) -> 'Exercise':
        '''Generate a SQL exercise based on the specified parameters.'''

        messages = llm.Message()
        messages.add_message_user(strings.prompt_generate(
            dataset_str=dataset.to_sql_no_context(),
            extra_details=extra_details,
            constraints=constraints,
            sql_dialect=sql_dialect,
            language=language,
            difficulty=difficulty
        ))

        # start with a lower temperature for more focused generation,
        # and increase it with each attempt to encourage more diversity in the generated solutions
        for _ in range(max_attempts):
            on_attempt_start()

            try:
                answer = llm.generate_answer(
                    messages,
                    json_format=llm.models.Assignment,
                    model=os.getenv('SQL_GENERATION_LLM_MODEL_EXERCISE', 'gpt-5.4-nano'),
                )
                assert isinstance(answer, llm.models.Assignment)
                
                # check syntax correctness of solution
                try:
                    query = Query(answer.solution, catalog=dataset.catalog)
                except Exception as e:
                    raise SQLParsingError(
                        TranslatableText(
                            f"Generated SQL solution contains syntax errors: {e}",
                            it=f"La soluzione SQL generata contiene errori di sintassi: {e}"
                        ).get(language),
                        answer.solution
                    )
                
                # execute the query to ensure it runs without errors
                with get_database(db_host, db_port, db_user, db_password, sql_dialect) as db:
                    try:
                        db.execute(dataset.to_sql_no_context())
                        db.execute(query.sql)
                    except QueryExecutionError as e:
                        raise SQLParsingError(
                            TranslatableText(
                                f"Generated SQL solution cannot be executed: {e}",
                                it=f"La soluzione SQL generata non può essere eseguita: {e}"
                            ).get(language),
                            query.sql
                        )

                # constraint validation
                constraint_errors = []
                
                for constraint in constraints:
                    try:
                        constraint.validate(query)
                    except ConstraintValidationError as e:
                        constraint_errors.append(e.get(language))

                if constraint_errors:
                    logger.debug(f'Constraint validation errors found: {constraint_errors}')
                    messages.add_message_user(strings.feedback_validation_errors(constraint_errors, language=language))
                    continue

                # refine natural language request to remove hints
                messages_refinement = llm.Message()
                messages_refinement.add_message_user(strings.prompt_refine_request(answer.request, query, language=language))
                answer_refinement = llm.generate_answer(
                    messages_refinement,
                    json_format=llm.models.RemoveHints,
                    model=os.getenv('SQL_GENERATION_LLM_MODEL_EXERCISE_NL_REQUEST', 'gpt-4o-mini')
                )

                assert isinstance(answer_refinement, llm.models.RemoveHints)
                answer.request = answer_refinement.request_without_hints

                result = Exercise(
                    title=title,
                    request=answer.request,
                    solutions=[query],
                    difficulty=difficulty,
                    error=error
                )

                return result

            except Exception as e:
                logger.debug(f'Error occurred while generating exercise: {e}')
                messages.add_message_user(
                    TranslatableText(
                        f"An error occurred: {str(e)}. Please regenerate valid JSON/SQL.",
                        it=f"Si è verificato un errore: {str(e)}. Per favore rigenera JSON/SQL valido."
                    ).get(language)
                )

        raise ExerciseGenerationError(f'Failed to generate a valid exercise for {error.name} after {max_attempts} attempts.')