'''Test script to generate an SQL assignment based on specified error, difficulty, and domain.'''

from sql_assignment_generator.difficulty_level import DifficultyLevel
from sql_error_categorizer import SqlErrors
from sql_assignment_generator import generate_assignment
from dotenv import load_dotenv



if __name__ == '__main__':
    load_dotenv()

    # change these values as needed
    domain = None
    errors = {
        SqlErrors.SYN_2_AMBIGUOUS_COLUMN: DifficultyLevel.HARD,
        SqlErrors.SYN_4_UNDEFINED_COLUMN: DifficultyLevel.HARD,
        SqlErrors.SYN_7_UNDEFINED_OBJECT: DifficultyLevel.HARD,
        SqlErrors.SEM_40_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION: DifficultyLevel.MEDIUM,
    }

    exercises_per_difficulty: dict[DifficultyLevel, int] = {}

    def name_exercise(error: SqlErrors, difficulty: DifficultyLevel) -> str:
        '''Generate a name for the exercise based on its index, error, and difficulty level.'''
        exercises_per_difficulty.setdefault(difficulty, 0)
        exercises_per_difficulty[difficulty] += 1
        index = exercises_per_difficulty[difficulty]

        if difficulty == DifficultyLevel.EASY:
            difficulty_str = 'A) Basic'
        elif difficulty == DifficultyLevel.MEDIUM:
            difficulty_str = 'B) Intermediate'
        else:
            difficulty_str = 'C) Advanced'
        return f'{difficulty_str} exercise #{index}'

    assignment = generate_assignment(errors=errors, domain=domain, shuffle_exercises=False, naming_func=name_exercise)
    print(assignment)
