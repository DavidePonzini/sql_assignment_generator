from collections import Counter
from .base import SchemaConstraint
from sqlglot import Expression, exp 


class HasCheckConstraint(SchemaConstraint):
    '''Requires the schema to have a specific number of CHECK constraints.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1) -> None:
        self.min_checks = min_tables
        self.max_checks = max_tables if max_tables > min_tables else -1

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        total_checks = 0
        
        for table in tables:
            checks_found = list(table.find_all(exp.Check, exp.CheckColumnConstraint))
            total_checks += len(checks_found)

        if self.max_checks < 0:
            return total_checks >= self.min_checks
        return self.min_checks <= total_checks <= self.max_checks
    
    @property
    def description(self) -> str:
        if self.max_checks < 0: 
            return f'Must have minimum {self.min_checks} CHECK constraints in schema'
        elif self.min_checks == self.max_checks: 
            return f'Must have exactly {self.min_checks} CHECK constraints in schema'
        else: 
            return f'Must have between {self.min_checks} and {self.max_checks} CHECK constraints in schema'
