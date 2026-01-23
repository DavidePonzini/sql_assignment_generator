from abc import ABC, abstractmethod
from sqlscope import Query

class BaseConstraint(ABC):
    '''Abstract base class for SQL query constraints.'''

    @abstractmethod
    def validate(self, query: Query) -> bool:
        '''
        Validate if the given SQL query satisfies the constraint.

        Args:
            query (Query): The SQL query to validate.
        Returns:
            bool: True if the query satisfies the constraint, False otherwise.
        '''

        pass

    @property
    @abstractmethod
    def description(self) -> str:
        '''Textual description of the constraint.'''

        pass