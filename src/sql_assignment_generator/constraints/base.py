from abc import ABC, abstractmethod
from sqlglot import Expression

class BaseConstraint(ABC):
    '''Abstract base class for SQL query constraints.'''

    @abstractmethod
    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        '''
        Validate if the given SQL query satisfies the constraint.

        Args:
            query_ast (Expression): The SQL query to validate.
            tables (list[Expression]): The list of table creation commands.
        Returns:
            bool: True if the query satisfies the constraint, False otherwise.
        '''

        pass

    @property
    @abstractmethod
    def description(self) -> str:
        '''Textual description of the constraint.'''

        pass