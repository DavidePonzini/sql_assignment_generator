from dotenv import load_dotenv
load_dotenv()

from sql_error_categorizer.sql_errors import SqlErrors
from .difficulty_level import DifficultyLevel
from . import generate_assignment


def main():
    """
    Funzione principale per generare e stampare un esercizio.
    """
    example_error = SqlErrors.LOG_76_EXTRANEOUS_ORDER_BY_CLAUSE
    example_difficulty = DifficultyLevel.HARD
    domain= None

    generate_assignment(domain, example_error, example_difficulty)


if __name__ == "__main__":
    main()