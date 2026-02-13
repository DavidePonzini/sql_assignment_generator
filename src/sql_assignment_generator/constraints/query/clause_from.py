from .base import QueryConstraint
from sqlscope import Query
from ...exceptions import ConstraintValidationError
from collections import Counter
from sqlglot import exp

class TableReferences(QueryConstraint):
    '''
    Requires the query to reference a specified number of different tables (either in FROM or JOIN clauses).
    '''

    def __init__(self, min_: int = 1, max_: int | None = None, *, allow_self_join: bool = False) -> None:
        self.min = min_
        self.max = max_
        self.allow_self_join = allow_self_join

    def validate(self, query: Query):
        #obtain all SELECT blocks in the query (main and subqueries)
        selects_collection = list(query.selects_collection.values()) if hasattr(query.selects, 'values') else query.selects

        for s in selects_collection:
            curr_select = s[1] if isinstance(s, tuple) else s
            if isinstance(curr_select, str): continue

            #count how many different tables are referenced in the FROM/JOIN clauses of this SELECT block
            tables_in_this_block = []
            select_ast = getattr(curr_select, 'ast', None)

            if select_ast is not None:
                #isolate the table of block to subquery
                for table_node in select_ast.find_all(exp.Table):
                    if table_node.find_ancestor(exp.Select) == select_ast:
                        if table_node.find_ancestor(exp.From) or table_node.find_ancestor(exp.Join):
                            tables_in_this_block.append(table_node.name.lower())
            else:
                #if ast is malformed use referenced_tables (select * FROM t1, t2)
                for table in getattr(curr_select, 'referenced_tables', []):
                    tables_in_this_block.append(table.real_name.lower())

            if not self.allow_self_join:
                tables_in_this_block = list(set(tables_in_this_block))
            
            table_count = len(tables_in_this_block)

            #validate single SELECT block based on min/max constraints
            if self.max is None:
                if table_count < self.min:
                    raise ConstraintValidationError(
                        f'A SELECT block in the query references {table_count} tables, '
                        f'but at least {self.min} are required. Tables: {tables_in_this_block}'
                    )
            elif not (self.min <= table_count <= self.max):
                raise ConstraintValidationError(
                    f'A SELECT block in the query references {table_count} tables, '
                    f'which is outside the allowed range of {self.min} to {self.max}. '
                    f'Tables found in block: {tables_in_this_block}'
                )

    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must have at least {self.min} tables in FROM (i.e., JOINs).'
        elif self.min == self.max:
            return f'Exercise must have exactly {self.min} tables in FROM (i.e., JOINs).'
        else:
            return f'Exercise must have between {self.min} and {self.max} tables in FROM (i.e., JOINs).'

class LeftJoin(QueryConstraint):
    '''
    Requires the presence of a Left JOINs.
    '''

    def validate(self, query: Query) -> None:
        for select in query.selects:
            for join in select.ast.find_all(exp.Join):
                # control side and join type
                kind = (join.kind or "").upper()
                side = (join.side or "").upper()

                if 'LEFT' in kind or 'LEFT' in side:
                    return
        
        raise ConstraintValidationError("Exercise does not require any LEFT JOIN operation.")
     
    @property
    def description(self) -> str:
        return "Exercise must require at least one LEFT JOIN operation."

class RightJoin(QueryConstraint):
    '''
    Requires the presence of a Right JOINs.
    '''

    def validate(self, query: Query) -> None:
        for select in query.selects:
            for join in select.ast.find_all(exp.Join):
                kind = (join.kind or "").upper()
                side = (join.side or "").upper()

                if 'RIGHT' in kind or 'RIGHT' in side:
                    return
        
        raise ConstraintValidationError("Exercise does not require any RIGHT JOIN operation.")
     
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
            if any(count > 1 for count in counts.values()): return
        
        raise ConstraintValidationError(
            f"No SELF JOIN detected. A self join requires referencing the same table multiple times "
            f"within the same clause. Referenced tables found: {table_names}"
        )
    
    @property
    def description(self) -> str:
        return "Exercise must require a SELF JOIN operation (joining a table to itself)."