from abc import ABC, abstractmethod
from sqlscope import Query
from sqlglot import exp

class BaseConstraint(ABC):
    '''Abstract base class for SQL query constraints.'''

    @property
    @abstractmethod
    def description(self) -> str:
        '''Textual description of the constraint, to be used in prompts.'''
        pass