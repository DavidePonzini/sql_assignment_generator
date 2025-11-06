from dotenv import load_dotenv
load_dotenv()

from sql_error_categorizer.sql_errors import SqlErrors
from .difficulty_level import DifficultyLevel
from . import generate_assignment


def main():
    """
    Funzione principale per generare e stampare un esercizio.
    """
    example_error = SqlErrors.SYN_21_COMPARISON_WITH_NULL
    example_difficulty = DifficultyLevel.HARD
    domain= None

    my_assignment = generate_assignment(domain, example_error, example_difficulty)
    #my_assignment.print_assignment()
    print(my_assignment)


if __name__ == "__main__":
    main()