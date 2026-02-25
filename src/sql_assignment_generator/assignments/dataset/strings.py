from typing import Sequence
from ...constraints import SchemaConstraint

def to_sql_format(schema: str, create_cmds: str, insert_cmds: str) -> str:
    return f'''BEGIN;

DROP SCHEMA IF EXISTS {schema} CASCADE;
CREATE SCHEMA {schema};
SET search_path TO {schema};

{create_cmds}

{insert_cmds}

COMMIT;'''


def prompt_generate(domain: str, extra_details: list[str], constraints: Sequence[SchemaConstraint]) -> str:
    formatted_constraints = '\n'.join(f'- {c.description}' for c in constraints)
   
    # remove empty extra details        
    extra_details = [detail for detail in extra_details if detail.strip() != '']
    # dataset characteristics str
    if len(extra_details) > 0:
        extra_details_str = "The dataset must have the following characteristics:\n"
        for detail in extra_details:
            extra_details_str += f"- {detail}\n"
    else:
        extra_details_str = ''
    
    return f'''
Generate a SQL dataset about the following domain: "{domain}".
{extra_details_str}

MANDATORY CONSTRAINTS:
- FOREIGN KEY attributes should have the REFERENCES keyword inline (e.g. "col TYPE REFERENCES table_name(column_name)").
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
'''

def feedback_constraint_violations(errors: list[str]) -> str:
    return (
        f"The previous JSON output was rejected because the SQL violated these constraints: {', '.join(errors)}\n"
        "Regenerate the JSON correcting the SQL to satisfy all mandatory constraints."
    )