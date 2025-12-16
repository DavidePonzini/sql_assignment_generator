from dataclasses import dataclass
import dav_tools

from sql_error_categorizer.sql_errors import SqlErrors
from ..sql_errors_details import ERROR_DETAILS_MAP
from ..difficulty_level import DifficultyLevel

@dataclass
class Dataset:
    create_commands: list[str]
    insert_commands: list[str]
    domain: str

    def to_sql(self, schema: str) -> str:
        '''Generate the SQL commands to create and populate the dataset within the specified schema.'''

        # Normalize schema name
        schema = schema.lower().replace(' ', '_')

        create_cmds = '\n'.join(self.create_commands)
        insert_cmds = '\n'.join(self.insert_commands)

        return f'''BEGIN;

DROP SCHEMA IF EXISTS {schema} CASCADE;
CREATE SCHEMA {schema};
SET search_path TO {schema};

{create_cmds}

{insert_cmds}

COMMIT;'''
    
    @staticmethod
    def generate(domain: str, errors: dict[SqlErrors, DifficultyLevel]) -> 'Dataset':
        dav_tools.messages.info(f'Generating dataset for domain: {domain}')

        create_commands = []
        insert_commands = []

        return Dataset(
            create_commands=create_commands,
            insert_commands=insert_commands,
            domain=domain
        )