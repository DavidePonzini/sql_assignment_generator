'''JSON models for LLM outputs.'''

from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class Assignment(BaseModel):
    '''JSON model for assignments'''
    
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
    '''JSON model for database schemas'''

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
    '''JSON model for removing hints from a request'''
    request_without_hints: str