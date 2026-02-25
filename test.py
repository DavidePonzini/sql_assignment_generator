'''Test script to generate an SQL assignment based on specified error, difficulty, and domain.'''

from src.sql_assignment_generator.difficulty_level import DifficultyLevel
from src.sql_assignment_generator import generate_assignment

from sql_error_taxonomy import SqlErrors
from dotenv import load_dotenv
import dav_tools


if __name__ == '__main__':
    load_dotenv()

    # change these values as needed
    domain = None
    errors = [
        (SqlErrors.SYN_22_OMITTING_THE_SEMICOLON, DifficultyLevel.EASY),
        (SqlErrors.SYN_2_AMBIGUOUS_COLUMN, DifficultyLevel.EASY),
    ]*3

    assignment = generate_assignment(errors, domain)
    
    dav_tools.messages.message(
        '-' * 50,
        assignment.dataset.to_sql('datasetExercise'),
        '-' * 50,
        default_text_options=[dav_tools.messages.TextFormat.Color.CYAN],
        sep='\n',
        additional_text_options=[
            [dav_tools.messages.TextFormat.Style.BOLD],
            [],
            [dav_tools.messages.TextFormat.Style.BOLD]
        ]
    )

    dav_tools.messages.message()
    
    for exercise in assignment.exercises:
        dav_tools.messages.message(
            exercise.title,
            default_text_options=[dav_tools.messages.TextFormat.Style.BOLD],
        )

        dav_tools.messages.message(
            exercise.request,
            icon_options=[dav_tools.messages.TextFormat.Color.BLUE, dav_tools.messages.TextFormat.Style.BOLD],
            icon='REQ',
        )
        for solution in exercise.solutions:
            dav_tools.messages.message(
                solution.sql,
                default_text_options=[dav_tools.messages.TextFormat.Color.LIGHTGRAY],
                icon_options=[dav_tools.messages.TextFormat.Color.GREEN, dav_tools.messages.TextFormat.Style.BOLD],
                icon='SOL',
            )

        dav_tools.messages.message()