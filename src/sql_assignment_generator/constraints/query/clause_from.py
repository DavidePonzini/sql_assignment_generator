from .base import QueryConstraint
from sqlglot import exp
from sqlscope import Query

class TableReferences(QueryConstraint):
    '''
    Requires the query to reference a specified number of different tables (either in FROM or JOIN clauses).
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> bool:
        referenced_tables: set[str] = set()

        for select in query.selects:
            for table in select.referenced_tables:
                referenced_tables.add(table.real_name)

        table_count = len(referenced_tables)
        if self.max is None:
            return table_count >= self.min
        return self.min <= table_count <= self.max
    
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

    def validate(self, query: Query) -> bool:
        # TODO

        for select in query.selects:
            # look for any LEFT JOIN node in the query and return True if found
            pass
        
        return True
    
        return False
     
    @property
    def description(self) -> str:
        return "Exercise must require at least one LEFT JOIN operation."

class RightJoin(QueryConstraint):
    '''
    Requires the presence of a Left JOINs.
    '''

    def validate(self, query: Query) -> bool:
        # TODO

        for select in query.selects:
            # look for any RIGHT JOIN node in the query and return True if found
            pass
        
        return True
    
        return False
     
    @property
    def description(self) -> str:
        return "Exercise must require at least one RIGHT JOIN operation."

class NoJoin(QueryConstraint):
    '''
    Requires the ABSENCE of any JOIN clause in the SQL query.
    '''

    def validate(self, query: Query) -> bool:
        from_tables = query.main_query.referenced_tables

        return len(from_tables) <= 1        
        
    
    @property
    def description(self) -> str:
        return "Must NOT have JOIN clause"
   