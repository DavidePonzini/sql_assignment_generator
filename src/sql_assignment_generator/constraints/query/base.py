from abc import abstractmethod
from ..base import BaseConstraint
from sqlscope import Query


class QueryConstraint(BaseConstraint):
    '''Base class for query-related constraints.'''
    
    @abstractmethod
    def validate(self, query: Query):
        '''
        Validate if the given SQL query satisfies the constraint.

        Args:
            query (Query): The SQL query to validate.
        Raises:
            ConstraintValidationError: If the query does not satisfy the constraint.
        '''
        pass