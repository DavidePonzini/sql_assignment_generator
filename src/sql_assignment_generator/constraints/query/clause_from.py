from .base import QueryConstraint
from sqlscope import Query
from ...exceptions import ConstraintValidationError
from collections import Counter
from sqlglot import exp
from ...translatable_text import TranslatableText

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
                    TranslatableText(
                       f'Exercise references {table_count} different tables ({referenced_tables}), which is less than the required minimum of {self.min} tables.',
                       it=f'L\'esercizio fa riferimento a {table_count} tabelle diverse ({referenced_tables}), che è meno del minimo richiesto di {self.min} tabelle.'
                    )
                )
        elif not (self.min <= table_count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Exercise references {table_count} different tables ({referenced_tables}), which is not within the required range of {self.min} to {self.max} tables.',
                    it=f'L\'esercizio fa riferimento a {table_count} tabelle diverse ({referenced_tables}), che non è compreso tra il minimo richiesto di {self.min} e il massimo di {self.max} tabelle.'
                )
            )

    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require referencing at least {self.min} different tables (i.e., JOINs).',
                it=f'L\'esercizio deve richiedere almeno {self.min} tabelle diverse (i.e., JOINs).'
            )
        elif self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} tables (i.e., JOINs).',
                it=f'L\'esercizio deve richiedere esattamente {self.min} tabelle (i.e., JOINs).'
            )
        else:
            return TranslatableText(
                f'Exercise must require between {self.min} and {self.max} tables (i.e., JOINs).',
                it=f'L\'esercizio deve richiedere tra {self.min} e {self.max} tabelle (i.e., JOINs).'
            )

class LeftJoin(QueryConstraint):
    '''
    Requires the presence of a Left JOINs.
    '''

    def validate(self, query: Query) -> None:
        for select in query.selects:
            ast = select.ast

            if ast is None:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Query parsing failed for SELECT clause: {select.sql}. Check if the SQL syntax is correct.',
                        it=f'Analisi della query fallita per la clausola SELECT: {select.sql}. Verifica che la sintassi SQL sia corretta.'
                    )
                )

            for join in ast.find_all(exp.Join):
                # control side and join type
                kind = (join.kind or '').upper()
                side = (join.side or '').upper()

                if 'LEFT' in kind or 'LEFT' in side:
                    return
        
        raise ConstraintValidationError(
            TranslatableText(
                'Exercise does not require any LEFT JOIN operation.',
                it='L\'esercizio non richiede alcun LEFT JOIN.'
            )
        )
     
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Exercise must require at least one LEFT JOIN operation.',
            it='L\'esercizio deve richiedere almeno un LEFT JOIN.'
        )

class RightJoin(QueryConstraint):
    '''
    Requires the presence of a Left JOINs.
    '''

    def validate(self, query: Query) -> None:
        for select in query.selects:
            ast = select.ast

            if ast is None:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Query parsing failed for SELECT clause: {select.sql}. Check if the SQL syntax is correct.',
                        it=f'Analisi della query fallita per la clausola SELECT: {select.sql}. Verifica che la sintassi SQL sia corretta.'
                    )
                )

            for join in ast.find_all(exp.Join):
                kind = (join.kind or '').upper()
                side = (join.side or '').upper()

                if 'RIGHT' in kind or 'RIGHT' in side:
                    return
        
        raise ConstraintValidationError(
            TranslatableText(
                'Exercise does not require any RIGHT JOIN operation.',
                it='L\'esercizio non richiede alcun RIGHT JOIN.'
            )
        )
     
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Exercise must require at least one RIGHT JOIN operation.',
            it='L\'esercizio deve richiedere almeno un RIGHT JOIN.'
        )

class NoJoin(QueryConstraint):
    '''
    Requires the ABSENCE of any JOIN clause in the SQL query.
    '''

    def validate(self, query: Query) -> None:
        from_tables = query.main_query.referenced_tables

        if len(from_tables) > 1:
            raise ConstraintValidationError(
                TranslatableText(
                    'Exercise references more than a single table, which implies the presence of JOIN clauses, which are not allowed.',
                    it='L\'esercizio fa riferimento a più di una tabella, il che implica la presenza di clausole JOIN, che non sono consentite.'
                )
            )
        
    
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Must NOT have JOIN clause',
            it='Non deve avere clausola JOIN'
        )

class SelfJoin(QueryConstraint):
    '''
    Requires the presence of a Self JOIN (joining a table with itself).
    '''

    def validate(self, query: Query) -> None:
        # iterate in main query and in subquery
        for select in query.selects:
            # extract name table and count all occurrences
            table_names = [table.real_name for table in select.referenced_tables]
            counts = Counter(table_names)

            # require at least one table to be referenced more than once (self join) 
            if not any(count > 1 for count in counts.values()):
                raise ConstraintValidationError(
                    TranslatableText(
                        'Exercise must require a SELF JOIN operation (joining a table to itself), but it does not.',
                        it='L\'esercizio deve richiedere un SELF JOIN (unire una tabella con se stessa), ma non lo fa.'
                    )
                )
    
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Exercise must require a SELF JOIN operation (joining a table to itself).',
            it='L\'esercizio deve richiedere un SELF JOIN (unire una tabella con se stessa).'
        )