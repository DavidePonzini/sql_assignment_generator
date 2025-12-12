'''Test script to generate an SQL assignment based on specified error, difficulty, and domain.'''

from sql_assignment_generator.sql_errors_details import ERROR_DETAILS_MAP
from sql_assignment_generator.difficulty_level import DifficultyLevel
from sql_assignment_generator import generate_assignment
import dav_tools
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    dav_tools.argument_parser.add_argument('error', type=int, help='SQL error to use.', choices=[e.value for e in ERROR_DETAILS_MAP.keys()])
    dav_tools.argument_parser.add_argument('difficulty', type=int, help='Difficulty level.', choices=[1, 2, 3])
    dav_tools.argument_parser.add_argument('domain', type=str, help='SQL error domain to use.', nargs='?', default=None)
    dav_tools.argument_parser.parse_args()

    error_id = dav_tools.argument_parser.args.error
    error_enum = next((e for e in ERROR_DETAILS_MAP.keys() if e.value == error_id))
    
    if dav_tools.argument_parser.args.difficulty == 1:
        difficulty_level = DifficultyLevel.EASY
    elif dav_tools.argument_parser.args.difficulty == 2:
        difficulty_level = DifficultyLevel.MEDIUM
    else:
        difficulty_level = DifficultyLevel.HARD

    domain = dav_tools.argument_parser.args.domain

    assignment = generate_assignment(error=error_enum, difficulty=difficulty_level, domain=domain)

    print(assignment)
