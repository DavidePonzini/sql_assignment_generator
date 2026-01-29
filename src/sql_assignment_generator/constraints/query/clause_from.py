from .base import QueryConstraint
from sqlglot import exp
from sqlscope import Query
from collections import Counter


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
        for select in query.selects:
            root_node = select.expression if hasattr(select, 'expression') else select

            for join in root_node.find_all(exp.Join):
                # controll side and join type
                kind = (join.kind or "").upper()
                side = (join.side or "").upper()

                if 'LEFT' in kind or 'LEFT' in side:
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
        for select in query.selects:
            root_node = select.expression if hasattr(select, 'expression') else select

            for join in root_node.find_all(exp.Join):
                kind = (join.kind or "").upper()
                side = (join.side or "").upper()

                if 'RIGHT' in kind or 'RIGHT' in side:
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

class SelfJoin(QueryConstraint):
    '''
    Requires the presence of a Self JOIN (joining a table with itself).
    '''

    def validate(self, query: Query) -> bool:
        # iterate in main query and in subquery
        for select in query.selects:
            # extract name table and count all occurrence
            table_names = [table.real_name for table in select.referenced_tables]
            counts = Counter(table_names)
            
            # table is repeat more than 1 
            if any(count > 1 for count in counts.values()):
                return True
        
        return False
    
    @property
    def description(self) -> str:
        return "Exercise must require a SELF JOIN operation (joining a table to itself)."