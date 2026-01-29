from ..base import BaseConstraint
from abc import abstractmethod
from sqlglot import exp
from sqlscope import Catalog

class SchemaConstraint(BaseConstraint):
    '''Base class for schema-related constraints.'''
    @abstractmethod
    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        '''
        Validate if the given table creation and insertion statements satisfy the constraint.

        Args:
            catalog (Catalog): The catalog representing the database schema.
            tables_sql (list[exp.Create]): List of CREATE TABLE expressions.
            values_sql (list[exp.Insert]): List of INSERT INTO expressions.
        Raises:
            ConstraintValidationError: If the schema does not satisfy the constraint.
        '''

        # TODO: one day I plan to use only sqlscope.Catalog here,
        # but for now we also keep the raw SQL expressions for checks not yet supported in sqlscope. 
        pass

    @abstractmethod
    def merge(self, other: 'SchemaConstraint') -> 'SchemaConstraint':
        '''Merges this constraint with another constraint of the same type.'''
        pass
