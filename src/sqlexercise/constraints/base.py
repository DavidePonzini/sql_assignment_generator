from abc import ABC, abstractmethod
from ..translatable_text import TranslatableText

class BaseConstraint(ABC):
    '''Abstract base class for SQL query constraints.'''

    @property
    @abstractmethod
    def description(self) -> TranslatableText:
        '''Textual description of the constraint, to be used in prompts.'''
        pass