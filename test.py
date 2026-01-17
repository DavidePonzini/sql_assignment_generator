'''Test script to generate an SQL assignment based on specified error, difficulty, and domain.'''

from sql_assignment_generator.difficulty_level import DifficultyLevel
from sql_error_categorizer import SqlErrors
from sql_assignment_generator import generate_assignment
from dotenv import load_dotenv
import dav_tools


if __name__ == '__main__':
    load_dotenv()

    # change these values as needed
    domain = None
    errors = [
        (SqlErrors.SEM_42_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES, DifficultyLevel.EASY),
        (SqlErrors.SEM_42_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES, DifficultyLevel.EASY),
        (SqlErrors.SEM_42_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES, DifficultyLevel.EASY),
    ]

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
                solution,
                default_text_options=[dav_tools.messages.TextFormat.Color.LIGHTGRAY],
                icon_options=[dav_tools.messages.TextFormat.Color.GREEN, dav_tools.messages.TextFormat.Style.BOLD],
                icon='SOL',
            )

        dav_tools.messages.message()