from typing import Sequence
from ...constraints import SchemaConstraint
from ...translatable_text import TranslatableText

def to_sql_format(schema: str, create_cmds: str, insert_cmds: str) -> str:
    return f'''BEGIN;

DROP SCHEMA IF EXISTS {schema} CASCADE;
CREATE SCHEMA {schema};
SET search_path TO {schema};

{create_cmds}

{insert_cmds}

COMMIT;'''


def prompt_generate(
        domain: str,
        extra_details: list[str],
        constraints: Sequence[SchemaConstraint],
        *,
        language: str
    ) -> str:
    formatted_constraints = '\n'.join(f'- {c.description.get(language)}' for c in constraints)
   
    # remove empty extra details        
    extra_details = [detail for detail in extra_details if detail.strip() != '']
    # dataset characteristics str
    if len(extra_details) > 0:
        extra_details_str = TranslatableText(
            "The dataset must have the following characteristics:\n",
            it="Il dataset deve avere le seguenti caratteristiche:\n"
        ).get(language)
        for detail in extra_details:
            extra_details_str += f"- {detail}\n"
    else:
        extra_details_str = ''
    
    return TranslatableText(
        f'''
Generate a SQL dataset about the following domain: "{domain}".
{extra_details_str}

MANDATORY CONSTRAINTS:
- FOREIGN KEY attributes should have the REFERENCES keyword inline (e.g. "col TYPE REFERENCES table_name(column_name)").
- VARCHAR columns should not have a length specified (e.g. use "col VARCHAR" instead of "col VARCHAR(255)").
{formatted_constraints}

MANDATORY OUTPUT (JSON) - each line in both lists must correspond to a single table:
{{
    "schema_tables": [
        "CREATE TABLE t1(...);",
        "CREATE TABLE t2(...);"
    ],
    "insert_commands": [
        "INSERT INTO t1(...) VALUES(val_1, val_2, ...), (...), (val_n, val_n+1, ...);",
        "INSERT INTO t2(...) VALUES(val_1, val_2, ...), (...), (val_n, val_n+1, ...);"
    ]
}}

INSERT INTO statements must have following format (Multi-row insert): 
INSERT INTO tableName(<all columns except SERIAL/AUTO_INCREMENT>) VALUES 
    (val_1, val_2, ...),
    (val_n, val_n+1, ...);

For each table, insert at least 5 rows of data.
Skip any SERIAL/AUTO_INCREMENT columns in the INSERT statements.
''',
        it=f'''Genera un dataset SQL sul seguente dominio: "{domain}".
{extra_details_str}

CONSTRAINT OBBLIGATORIE:
- Gli attributi FOREIGN KEY devono avere la keyword REFERENCES inline (es. "col TYPE REFERENCES table_name(column_name)").
- Le colonne VARCHAR non devono avere una lunghezza specificata (es. usa "col VARCHAR" invece di "col VARCHAR(255)").
{formatted_constraints}

OUTPUT OBBLIGATORIO (JSON) - ogni riga in entrambe le liste deve corrispondere a una singola tabella:
{{
    "schema_tables": [
        "CREATE TABLE t1(...);",
        "CREATE TABLE t2(...);"
    ],
    "insert_commands": [
        "INSERT INTO t1(...) VALUES(val_1, val_2, ...), (...), (val_n, val_n+1, ...);",
        "INSERT INTO t2(...) VALUES(val_1, val_2, ...), (...), (val_n, val_n+1, ...);"
    ]
}}

Le istruzioni INSERT INTO devono avere il seguente formato (Multi-row insert):
INSERT INTO tableName(<tutte le colonne tranne SERIAL/AUTO_INCREMENT>) VALUES
    (val_1, val_2, ...),
    (val_n, val_n+1, ...);

Per ogni tabella, inserisci almeno 5 righe di dati.
''',
    ).get(language)

def feedback_constraint_violations(errors: list[str], * , language: str) -> str:
    return TranslatableText(
        f"The previous JSON output was rejected because the SQL violated these constraints: {', '.join(errors)}\n Regenerate the JSON correcting the SQL to satisfy all mandatory constraints.",
        it=f"Il precedente output JSON è stato rifiutato perché il SQL ha violato queste constraint: {', '.join(errors)}\n Rigenera il JSON correggendo il SQL per soddisfare tutte le constraint obbligatorie."
    ).get(language)