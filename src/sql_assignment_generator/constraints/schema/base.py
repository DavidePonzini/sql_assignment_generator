from ..base import BaseConstraint
from abc import abstractmethod

class SchemaConstraint(BaseConstraint):
    '''Base class for schema-related constraints.'''
    pass

    @abstractmethod
    def merge(self, other: 'SchemaConstraint') -> 'SchemaConstraint':
        '''Merges this constraint with another constraint of the same type.'''
        pass
