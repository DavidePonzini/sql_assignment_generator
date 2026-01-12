from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class Assignment(BaseModel):
    request: str
    solution: str

    def __str__(self) -> str:
        return f'''
Request:
{self.request}

Solution:
{self.solution}
'''



@dataclass
class Schema(BaseModel):
    schema_tables: list[str]
    insert_commands: list[str]

    def __str__(self) -> str:
        tables = '\n'.join(self.schema_tables)
        value = '\n'.join(self.insert_commands)

        return f'''
Schema Tables:
{tables}

Insert Value:
{value}
'''
    
@dataclass
class RemoveHints(BaseModel):
    request_without_hints: str