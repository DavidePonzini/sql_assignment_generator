"""Test script per generare assignment SQL, stampare dataset ed esercizi
come nel file originale, e salvare un CSV riassuntivo con una sola riga
per ciascuna coppia (error_id, difficulty).

Formato riepilogo:
ERRORE ID: {error_id} | DIFFICOLTÀ: {difficulty_str} | GENERATI: {n} | NON_GENERATI: {m}
"""

from collections import defaultdict
from pathlib import Path
import csv

from src.sql_assignment_generator.difficulty_level import DifficultyLevel
from src.sql_assignment_generator import generate_assignment

from sql_error_taxonomy import SqlErrors
from dotenv import load_dotenv
import dav_tools


def get_error_id(error_obj):
    if hasattr(error_obj, "name"):
        return error_obj.name
    if hasattr(error_obj, "value"):
        return str(error_obj.value)
    return str(error_obj)


def parse_title(title: str):
    """
    Estrae error_id e difficulty dal titolo dell'esercizio.
    Esempio:
    'SYN_19_USING_WHERE_TWICE - MEDIUM'
    -> ('SYN_19_USING_WHERE_TWICE', 'MEDIUM')
    """
    if ' - ' not in title:
        return None, None

    left, right = title.rsplit(' - ', 1)
    return left.strip(), right.strip()


if __name__ == '__main__':
    load_dotenv()

    domain = None
    errors = [
        (SqlErrors.LOG_71_MISSING_COLUMN_FROM_SELECT, DifficultyLevel.EASY),
        (SqlErrors.LOG_71_MISSING_COLUMN_FROM_SELECT, DifficultyLevel.MEDIUM),
        (SqlErrors.LOG_71_MISSING_COLUMN_FROM_SELECT, DifficultyLevel.HARD),
    ] * 10

    assignment = generate_assignment(
        errors,
        domain=domain,
        language='en',
    )

    script_dir = Path(__file__).resolve().parent
    csv_dir = script_dir / 'CSV'
    csv_dir.mkdir(parents=True, exist_ok=True)

    first_error_id = get_error_id(errors[0][0])
    csv_path = csv_dir / f'{first_error_id}.csv'

    # STAMPA DATASET
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

    # STAMPA ESERCIZI COME NEL FILE ORIGINALE
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

    # CONTEGGI RICHIESTI
    requested_counts = defaultdict(int)
    for error_obj, difficulty in errors:
        error_id = get_error_id(error_obj)
        difficulty_str = difficulty.name if hasattr(difficulty, "name") else str(difficulty)
        requested_counts[(error_id, difficulty_str)] += 1

    # CONTEGGI GENERATI REALI, LEGGENDO IL TITOLO DELL'ESERCIZIO
    generated_counts = defaultdict(int)
    for exercise in assignment.exercises:
        parsed_error_id, parsed_difficulty = parse_title(exercise.title)

        if parsed_error_id is None or parsed_difficulty is None:
            continue

        generated_counts[(parsed_error_id, parsed_difficulty)] += 1

    csv_rows = []

    # STAMPA RIEPILOGO
    dav_tools.messages.message(
        'RIEPILOGO GENERAZIONE',
        default_text_options=[dav_tools.messages.TextFormat.Style.BOLD],
    )

    for (error_id, difficulty_str), requested in requested_counts.items():
        generated = generated_counts.get((error_id, difficulty_str), 0)
        not_generated = requested - generated

        dav_tools.messages.message(
            f'ERRORE ID: {error_id} | DIFFICOLTÀ: {difficulty_str} | GENERATI: {generated} | NON_GENERATI: {not_generated}',
            icon_options=[dav_tools.messages.TextFormat.Color.BLUE, dav_tools.messages.TextFormat.Style.BOLD],
            icon='SUM',
        )

        csv_rows.append({
            'error_id': error_id,
            'difficulty': difficulty_str,
            'generati': generated,
            'non_generati': not_generated,
        })

    # SCRITTURA CSV
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                'error_id',
                'difficulty',
                'generati',
                'non_generati',
            ],
            delimiter=';'
        )
        writer.writeheader()
        writer.writerows(csv_rows)

    # MESSAGGIO FINALE
    if csv_path.exists():
        dav_tools.messages.message(
            f'CSV creato correttamente: {csv_path}',
            icon_options=[dav_tools.messages.TextFormat.Color.GREEN, dav_tools.messages.TextFormat.Style.BOLD],
            icon='CSV',
        )
    else:
        dav_tools.messages.message(
            f'Errore: il CSV non risulta creato in {csv_path}',
            icon_options=[dav_tools.messages.TextFormat.Color.BLUE, dav_tools.messages.TextFormat.Style.BOLD],
            icon='ERR',
        )

    print(f'CSV_PATH_ASSOLUTO: {csv_path}')