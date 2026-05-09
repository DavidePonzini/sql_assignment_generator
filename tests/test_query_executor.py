import pytest
from unittest.mock import patch, MagicMock
from sql_assignment_generator.query_executor import (
    execute_query,
    validate_assignment,
    ExecutionResult,
)
from sql_assignment_generator.assignments import Assignment, Dataset, Exercise
from sql_assignment_generator.difficulty_level import DifficultyLevel
from sql_error_taxonomy import SqlErrors
from sqlscope import Query
from sql_assignment_generator.db.exceptions import QueryExecutionError


def _make_dataset(create_sqls: list[str], insert_sqls: list[str]) -> Dataset:
    '''Create a Dataset from raw SQL strings.'''
    return Dataset.from_sql(
        sql_str='\n'.join(create_sqls + insert_sqls),
        sql_dialect='postgres',
    )


# =================================================================
# EXECUTION RESULT
# =================================================================

class TestExecutionResult:

    def test_has_results_true(self):
        r = ExecutionResult(rows=[(1,)])
        assert r.has_results
        assert r.success

    def test_has_results_false_empty(self):
        r = ExecutionResult(rows=[])
        assert not r.has_results
        assert r.success

    def test_has_results_false_error(self):
        r = ExecutionResult(rows=[], error='some error')
        assert not r.has_results
        assert not r.success


# =================================================================
# EXECUTE QUERY
# =================================================================

class TestExecuteQuery:

    def test_returns_results(self):
        db = MagicMock()
        db.execute.return_value = [(1, 10), (2, 20)]
        result = execute_query(db, 'SELECT * FROM t1')
        assert result.success
        assert result.has_results
        assert len(result.rows) == 2

    def test_returns_empty(self):
        db = MagicMock()
        db.execute.return_value = []
        result = execute_query(db, 'SELECT * FROM t1 WHERE val > 100')
        assert result.success
        assert not result.has_results

    def test_query_error(self):
        db = MagicMock()
        db.execute.side_effect = QueryExecutionError('table not found')
        result = execute_query(db, 'SELECT * FROM nonexistent')
        assert not result.success
        assert result.error is not None


# =================================================================
# VALIDATE ASSIGNMENT
# =================================================================

class TestValidateAssignment:

    @patch('sql_assignment_generator.query_executor.get_database')
    def test_all_exercises_return_results(self, mock_get_db):
        dataset = _make_dataset(
            ['CREATE TABLE t1 (id INT PRIMARY KEY, val INT);'],
            ['INSERT INTO t1 (id, val) VALUES (1, 10), (2, 20);'],
        )
        catalog = dataset.catalog
        query = Query('SELECT * FROM t1 WHERE val > 5', catalog=catalog)
        exercise = Exercise(
            title='Test',
            request='Get all rows with val > 5',
            solutions=[query],
            difficulty=DifficultyLevel.EASY,
            error=SqlErrors.SYN_1_OMITTING_CORRELATION_NAMES,
        )
        assignment = Assignment(dataset=dataset, exercises=[exercise])

        mock_db = MagicMock()
        mock_db.execute.return_value = [(1, 10), (2, 20)]
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_get_db.return_value = mock_db

        results = validate_assignment(assignment, 'postgres', 'h', 5432, 'u', 'p')
        assert len(results) == 1
        _, result = results[0]
        assert result.has_results

    @patch('sql_assignment_generator.query_executor.get_database')
    def test_exercise_returns_no_results(self, mock_get_db):
        dataset = _make_dataset(
            ['CREATE TABLE t1 (id INT PRIMARY KEY, val INT);'],
            ['INSERT INTO t1 (id, val) VALUES (1, 10), (2, 20);'],
        )
        catalog = dataset.catalog
        query = Query('SELECT * FROM t1 WHERE val > 100', catalog=catalog)
        exercise = Exercise(
            title='Test',
            request='Get all rows with val > 100',
            solutions=[query],
            difficulty=DifficultyLevel.EASY,
            error=SqlErrors.SYN_1_OMITTING_CORRELATION_NAMES,
        )
        assignment = Assignment(dataset=dataset, exercises=[exercise])

        mock_db = MagicMock()
        # First call loads dataset, second call executes query returning empty
        mock_db.execute.side_effect = [None, []]
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_get_db.return_value = mock_db

        results = validate_assignment(assignment, 'postgres', 'h', 5432, 'u', 'p')
        assert len(results) == 1
        _, result = results[0]
        assert result.success
        assert not result.has_results

    @patch('sql_assignment_generator.query_executor.get_database')
    def test_multiple_exercises_mixed(self, mock_get_db):
        dataset = _make_dataset(
            ['CREATE TABLE t1 (id INT PRIMARY KEY, val INT);'],
            ['INSERT INTO t1 (id, val) VALUES (1, 10), (2, 20);'],
        )
        catalog = dataset.catalog
        q_ok = Query('SELECT * FROM t1 WHERE val > 5', catalog=catalog)
        q_empty = Query('SELECT * FROM t1 WHERE val > 100', catalog=catalog)
        exercises = [
            Exercise(
                title='OK',
                request='r1',
                solutions=[q_ok],
                difficulty=DifficultyLevel.EASY,
                error=SqlErrors.SYN_1_OMITTING_CORRELATION_NAMES,
            ),
            Exercise(
                title='Empty',
                request='r2',
                solutions=[q_empty],
                difficulty=DifficultyLevel.EASY,
                error=SqlErrors.SYN_1_OMITTING_CORRELATION_NAMES,
            ),
        ]
        assignment = Assignment(dataset=dataset, exercises=exercises)

        mock_db = MagicMock()
        # 1st call: dataset load, 2nd: q_ok returns rows, 3rd: q_empty returns empty
        mock_db.execute.side_effect = [None, [(1, 10), (2, 20)], []]
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_get_db.return_value = mock_db

        results = validate_assignment(assignment, 'postgres', 'h', 5432, 'u', 'p')
        assert len(results) == 2
        assert results[0][1].has_results
        assert not results[1][1].has_results

    @patch('sql_assignment_generator.query_executor.get_database')
    def test_dataset_load_failure(self, mock_get_db):
        dataset = _make_dataset(
            ['CREATE TABLE t1 (id INT PRIMARY KEY);'],
            ['INSERT INTO t1 (id) VALUES (1);'],
        )
        catalog = dataset.catalog
        query = Query('SELECT * FROM t1', catalog=catalog)
        exercise = Exercise(
            title='Test',
            request='r',
            solutions=[query],
            difficulty=DifficultyLevel.EASY,
            error=SqlErrors.SYN_1_OMITTING_CORRELATION_NAMES,
        )
        assignment = Assignment(dataset=dataset, exercises=[exercise])

        mock_db = MagicMock()
        mock_db.execute.side_effect = QueryExecutionError('schema error')
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_get_db.return_value = mock_db

        results = validate_assignment(assignment, 'postgres', 'h', 5432, 'u', 'p')
        assert len(results) == 1
        _, result = results[0]
        assert not result.success
        assert 'Dataset failed to load' in result.error
