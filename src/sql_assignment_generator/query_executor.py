'''Execute SQL queries against a dataset using an in-memory SQLite database.'''

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

import sqlglot

from .assignments import Assignment, Dataset, Exercise


@dataclass
class ExecutionResult:
    '''Result of executing a single query.'''

    rows: list[tuple]
    columns: list[str]
    error: str | None = None

    @property
    def has_results(self) -> bool:
        return self.error is None and len(self.rows) > 0

    @property
    def success(self) -> bool:
        return self.error is None


def _transpile(sql: str, read_dialect: str) -> str | None:
    '''Transpile SQL from the source dialect to SQLite. Returns None on failure.'''
    try:
        results = sqlglot.transpile(sql, read=read_dialect, write='sqlite')
        return results[0] if results else None
    except Exception:
        return None


def create_db(dataset: Dataset, sql_dialect: str) -> sqlite3.Connection:
    '''Create an in-memory SQLite database from a dataset's CREATE and INSERT commands.'''
    conn = sqlite3.connect(':memory:')

    for cmd in dataset.create_commands:
        sqlite_sql = _transpile(cmd, sql_dialect)
        if sqlite_sql is None:
            sqlite_sql = cmd  # fall back to original SQL
        try:
            conn.execute(sqlite_sql)
        except Exception:
            pass  # skip untranslatable statements

    for cmd in dataset.insert_commands:
        sqlite_sql = _transpile(cmd, sql_dialect)
        if sqlite_sql is None:
            sqlite_sql = cmd
        try:
            conn.execute(sqlite_sql)
        except Exception:
            pass

    conn.commit()
    return conn


def execute_query(conn: sqlite3.Connection, query_sql: str, sql_dialect: str) -> ExecutionResult:
    '''Execute a single query and return the result.'''
    sqlite_sql = _transpile(query_sql, sql_dialect)
    if sqlite_sql is None:
        sqlite_sql = query_sql
    try:
        cursor = conn.execute(sqlite_sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        return ExecutionResult(rows=rows, columns=columns)
    except Exception as e:
        return ExecutionResult(rows=[], columns=[], error=str(e))


def validate_assignment(assignment: Assignment, sql_dialect: str) -> list[tuple[Exercise, ExecutionResult]]:
    '''Execute all exercises' solutions and return results.

    Returns a list of (exercise, result) tuples in the same order as exercises.
    '''
    results: list[tuple[Exercise, ExecutionResult]] = []
    conn = create_db(assignment.dataset, sql_dialect)

    for exercise in assignment.exercises:
        query_sql = exercise.solutions[0].sql
        result = execute_query(conn, query_sql, sql_dialect)
        results.append((exercise, result))

    conn.close()
    return results
