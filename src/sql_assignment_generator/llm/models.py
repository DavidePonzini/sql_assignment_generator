from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class Assignment(BaseModel):
    request: str
    solution: str
    schema_tables: list[str]

    def __str__(self) -> str:
        tables = '\n'.join(self.schema_tables)

        return f'''
Schema Tables:
{tables}

Request:
{self.request}

Solution:
{self.solution}
'''
