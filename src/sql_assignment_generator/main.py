from dotenv import load_dotenv
load_dotenv()

from sql_error_categorizer.sql_errors import SqlErrors
from .difficulty_level import DifficultyLevel
from . import generate_assignment


def main():
    """
    Funzione principale per generare e stampare un esercizio.
    """
    example_error = SqlErrors.SEM_45_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL
    example_difficulty = DifficultyLevel.HARD
    domain= None

    generate_assignment(domain, example_error, example_difficulty)


if __name__ == "__main__":
    main()