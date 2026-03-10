"""Test per la generazione del DB.

Produce due test:

1) 1xN
   - genera 1 dataset contenente N esercizi
   - ripete il test 5 volte

2) NxN
   - genera N dataset separati, uno per ogni errore richiesto

Salva un CSV riassuntivo in:
./CSV/DB_test.csv

Colonne CSV:
dataset_type;dataset_domain;dataset_generati;dataset_falliti
"""

from pathlib import Path
import csv

from dotenv import load_dotenv

from src.sql_assignment_generator import generate_assignment
from src.sql_assignment_generator.difficulty_level import DifficultyLevel
from sql_error_taxonomy import SqlErrors

import dav_tools


RUNS_1xN = 10


def dataset_generated_successfully(assignment) -> bool:
    """Controlla se il dataset è stato generato correttamente."""
    try:
        if assignment is None:
            return False

        if not hasattr(assignment, 'dataset') or assignment.dataset is None:
            return False

        dataset_sql = assignment.dataset.to_sql('datasetExercise')

        if dataset_sql is None:
            return False

        if not str(dataset_sql).strip():
            return False

        return True
    except Exception:
        return False


def domain_to_string(domain):
    if domain is None:
        return 'None'
    return str(domain)


if __name__ == '__main__':
    load_dotenv()

    domain = None

    errors = [
        (SqlErrors.SYN_2_AMBIGUOUS_COLUMN, DifficultyLevel.EASY),
        (SqlErrors.SYN_4_UNDEFINED_COLUMN, DifficultyLevel.MEDIUM),
        (SqlErrors.SYN_7_UNDEFINED_OBJECT, DifficultyLevel.HARD),
        (SqlErrors.SYN_9_MISSPELLINGS, DifficultyLevel.EASY),
        (SqlErrors.SYN_15_AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED, DifficultyLevel.MEDIUM),
        (SqlErrors.SYN_19_USING_WHERE_TWICE, DifficultyLevel.HARD),
        (SqlErrors.SYN_21_COMPARISON_WITH_NULL, DifficultyLevel.EASY),
        (SqlErrors.LOG_71_MISSING_COLUMN_FROM_SELECT, DifficultyLevel.MEDIUM),
        (SqlErrors.COM_97_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT, DifficultyLevel.HARD),
        (SqlErrors.LOG_62_MISSING_JOIN, DifficultyLevel.HARD),
    ]

    script_dir = Path(__file__).resolve().parent
    csv_dir = script_dir / 'CSV'
    csv_dir.mkdir(parents=True, exist_ok=True)

    csv_path = csv_dir / 'DB_test.csv'

    csv_rows = []

    # =========================
    # TEST 1xN
    # =========================

    dataset_generati_1xN = 0
    dataset_falliti_1xN = 0

    dav_tools.messages.message(
        'TEST DB 1xN',
        default_text_options=[dav_tools.messages.TextFormat.Style.BOLD],
    )

    for run_idx in range(1, RUNS_1xN + 1):
        try:
            assignment = generate_assignment(
                errors,
                domain=domain,
                language='en',
            )

            if dataset_generated_successfully(assignment):
                dataset_generati_1xN += 1

                dav_tools.messages.message(
                    f'Run {run_idx}: dataset generato',
                    icon='OK',
                    icon_options=[
                        dav_tools.messages.TextFormat.Color.GREEN,
                        dav_tools.messages.TextFormat.Style.BOLD,
                    ],
                )
            else:
                dataset_falliti_1xN += 1

                dav_tools.messages.message(
                    f'Run {run_idx}: dataset fallito',
                    icon='ERR',
                    icon_options=[
                        dav_tools.messages.TextFormat.Color.BLUE,
                        dav_tools.messages.TextFormat.Style.BOLD,
                    ],
                )

        except Exception as exc:
            dataset_falliti_1xN += 1

            dav_tools.messages.message(
                f'Run {run_idx}: errore durante la generazione -> {exc}',
                icon='ERR',
                icon_options=[
                    dav_tools.messages.TextFormat.Color.BLUE,
                    dav_tools.messages.TextFormat.Style.BOLD,
                ],
            )

    csv_rows.append({
        'dataset_type': '1xN',
        'dataset_generati': dataset_generati_1xN,
        'dataset_falliti': dataset_falliti_1xN,
    })

    dav_tools.messages.message()

    # =========================
    # TEST NxN
    # =========================

    dataset_generati_NxN = 0
    dataset_falliti_NxN = 0

    dav_tools.messages.message(
        'TEST DB NxN',
        default_text_options=[dav_tools.messages.TextFormat.Style.BOLD],
    )

    for idx, single_error in enumerate(errors, start=1):
        try:
            assignment = generate_assignment(
                [single_error],
                domain=domain,
                language='en',
            )

            if dataset_generated_successfully(assignment):
                dataset_generati_NxN += 1

                dav_tools.messages.message(
                    f'Dataset {idx}: generato',
                    icon='OK',
                    icon_options=[
                        dav_tools.messages.TextFormat.Color.GREEN,
                        dav_tools.messages.TextFormat.Style.BOLD,
                    ],
                )
            else:
                dataset_falliti_NxN += 1

                dav_tools.messages.message(
                    f'Dataset {idx}: fallito',
                    icon='ERR',
                    icon_options=[
                        dav_tools.messages.TextFormat.Color.BLUE,
                        dav_tools.messages.TextFormat.Style.BOLD,
                    ],
                )

        except Exception as exc:
            dataset_falliti_NxN += 1

            dav_tools.messages.message(
                f'Dataset {idx}: errore durante la generazione -> {exc}',
                icon='ERR',
                icon_options=[
                    dav_tools.messages.TextFormat.Color.BLUE,
                    dav_tools.messages.TextFormat.Style.BOLD,
                ],
            )

    csv_rows.append({
        'dataset_type': 'NxN',
        'dataset_generati': dataset_generati_NxN,
        'dataset_falliti': dataset_falliti_NxN,
    })

    dav_tools.messages.message()

    # =========================
    # SCRITTURA CSV
    # =========================

    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                'dataset_type',
                'dataset_domain',
                'dataset_generati',
                'dataset_falliti',
            ],
            delimiter=';'
        )
        writer.writeheader()
        writer.writerows(csv_rows)

    dav_tools.messages.message(
        f'CSV salvato in: {csv_path}',
        icon='CSV',
        icon_options=[
            dav_tools.messages.TextFormat.Color.GREEN,
            dav_tools.messages.TextFormat.Style.BOLD,
        ],
    )