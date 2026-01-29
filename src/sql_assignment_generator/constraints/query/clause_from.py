from .base import QueryConstraint
from sqlscope import Query
from ...exceptions import ConstraintValidationError

class TableReferences(QueryConstraint):
    '''
    Requires the query to reference a specified number of different tables (either in FROM or JOIN clauses).
    '''

    def __init__(self, min_: int = 1, max_: int | None = None, *, allow_self_join: bool = False) -> None:
        self.min = min_
        self.max = max_
        self.allow_self_join = allow_self_join

    def validate(self, query: Query):
        referenced_tables: list[str] = []

        for select in query.selects:
            for table in select.referenced_tables:
                referenced_tables.append(table.real_name)

        if not self.allow_self_join:
            referenced_tables = list(set(referenced_tables))
        table_count = len(referenced_tables)
            
        if self.max is None:
            if table_count < self.min:
                raise ConstraintValidationError(
                    f'Exercise references {table_count} different tables ({referenced_tables}), which is less than the required minimum of {self.min} tables.'
                )
        elif not (self.min <= table_count <= self.max):
            raise ConstraintValidationError(
                f'Exercise references {table_count} different tables ({referenced_tables}), which is not within the required range of {self.min} to {self.max} tables.'
            )

    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require referencing at least {self.min} different tables (i.e., JOINs).'
        elif self.min == self.max:
            return f'Exercise must require exactly {self.min} tables (i.e., JOINs).'
        else:
            return f'Exercise must require between {self.min} and {self.max} tables (i.e., JOINs).'


class LeftJoin(QueryConstraint):
    '''
    Requires the presence of a Left JOINs.
    '''

    def validate(self, query: Query) -> None:
        # TODO

        for select in query.selects:
            # look for any LEFT JOIN node in the query and raise an exception if found
            pass
        
     
    @property
    def description(self) -> str:
        return "Exercise must require at least one LEFT JOIN operation."

class RightJoin(QueryConstraint):
    '''
    Requires the presence of a Left JOINs.
    '''

    def validate(self, query: Query) -> None:
        # TODO

        for select in query.selects:
            # look for any RIGHT JOIN node in the query and raise an exception if found
            pass
     
    @property
    def description(self) -> str:
        return "Exercise must require at least one RIGHT JOIN operation."

class NoJoin(QueryConstraint):
    '''
    Requires the ABSENCE of any JOIN clause in the SQL query.
    '''

    def validate(self, query: Query) -> None:
        from_tables = query.main_query.referenced_tables

        if len(from_tables) > 1:
            raise ConstraintValidationError("Exercise references more than a single table, which implies the presence of JOIN clauses, which are not allowed.")
        
    
    @property
    def description(self) -> str:
        return "Must NOT have JOIN clause"
   