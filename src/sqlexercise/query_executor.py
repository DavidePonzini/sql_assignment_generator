'''Execute SQL queries against a dataset using the configured DBMS.'''

from __future__ import annotations

from dataclasses import dataclass

from sqlscope import Dialect

from .assignments import Assignment, Exercise
from .db import get_database, Database, QueryExecutionError


@dataclass
class ExecutionResult:
    '''Result of executing a single query.'''

    rows: list[tuple]
    error: str | None = None

    @property
    def has_results(self) -> bool:
        return self.error is None and len(self.rows) > 0

    @property
    def success(self) -> bool:
        return self.error is None


def execute_query(db: Database, query_sql: str) -> ExecutionResult:
    '''Execute a single query and return the result.'''
    try:
        rows = db.execute(query_sql)
        return ExecutionResult(rows=rows)
    except QueryExecutionError as e:
        return ExecutionResult(rows=[], error=str(e))


def validate_assignment(
        assignment: Assignment,
        sql_dialect: Dialect,
        db_host: str,
        db_port: int,
        db_user: str,
        db_password: str,
    ) -> list[tuple[Exercise, ExecutionResult]]:
    '''Execute all exercises' solutions against the dataset and return results.

    Creates a temporary schema on the DBMS, loads the dataset, executes each
    exercise query, then cleans up the schema.
    '''
    results: list[tuple[Exercise, ExecutionResult]] = []

    with get_database(db_host, db_port, db_user, db_password, sql_dialect) as db:
        # Load dataset into the temporary schema
        dataset_sql = assignment.dataset.to_sql_no_context()
        try:
            db.execute(dataset_sql)
        except QueryExecutionError:
            # Dataset itself failed to load — all queries will fail
            for exercise in assignment.exercises:
                results.append((exercise, ExecutionResult(rows=[], error='Dataset failed to load')))
            return results

        # Execute each exercise query
        for exercise in assignment.exercises:
            query_sql = exercise.solutions[0].sql
            result = execute_query(db, query_sql)
            results.append((exercise, result))

    return results
