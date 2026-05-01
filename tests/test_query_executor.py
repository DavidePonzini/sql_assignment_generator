import pytest
from sql_assignment_generator.query_executor import (
    create_db,
    execute_query,
    validate_assignment,
    ExecutionResult,
)
from sql_assignment_generator.assignments import Assignment, Dataset, Exercise
from sql_assignment_generator.difficulty_level import DifficultyLevel
from sql_error_taxonomy import SqlErrors
from sqlscope import Query


def _make_dataset(create_sqls: list[str], insert_sqls: list[str]) -> Dataset:
    '''Create a Dataset from raw SQL strings.'''
    return Dataset.from_sql(
        sql_str='\n'.join(create_sqls + insert_sqls),
        sql_dialect='postgres',
    )


# =================================================================
# CREATE DB
# =================================================================

class TestCreateDb:

    def test_basic_schema_and_data(self):
        dataset = _make_dataset(
            ['CREATE TABLE t1 (id INT PRIMARY KEY, name VARCHAR);'],
            ["INSERT INTO t1 (id, name) VALUES (1, 'Alice'), (2, 'Bob');"],
        )
        conn = create_db(dataset, 'postgres')
        rows = conn.execute('SELECT * FROM t1').fetchall()
        conn.close()
        assert len(rows) == 2
        assert rows[0] == (1, 'Alice')

    def test_multiple_tables(self):
        dataset = _make_dataset(
            [
                'CREATE TABLE t1 (id INT PRIMARY KEY);',
                'CREATE TABLE t2 (id INT PRIMARY KEY, name VARCHAR);',
            ],
            [
                'INSERT INTO t1 (id) VALUES (1), (2);',
                "INSERT INTO t2 (id, name) VALUES (1, 'x'), (2, 'y');",
            ],
        )
        conn = create_db(dataset, 'postgres')
        t1_rows = conn.execute('SELECT * FROM t1').fetchall()
        t2_rows = conn.execute('SELECT * FROM t2').fetchall()
        conn.close()
        assert len(t1_rows) == 2
        assert len(t2_rows) == 2

    def test_foreign_key(self):
        dataset = _make_dataset(
            [
                'CREATE TABLE dept (id INT PRIMARY KEY, name VARCHAR);',
                'CREATE TABLE emp (id INT PRIMARY KEY, dept_id INT REFERENCES dept(id));',
            ],
            [
                "INSERT INTO dept (id, name) VALUES (1, 'Engineering');",
                "INSERT INTO emp (id, dept_id) VALUES (1, 1), (2, 1);",
            ],
        )
        conn = create_db(dataset, 'postgres')
        rows = conn.execute('SELECT * FROM emp').fetchall()
        conn.close()
        assert len(rows) == 2


# =================================================================
# EXECUTE QUERY
# =================================================================

class TestExecuteQuery:

    def test_returns_results(self):
        dataset = _make_dataset(
            ['CREATE TABLE t1 (id INT PRIMARY KEY, val INT);'],
            ['INSERT INTO t1 (id, val) VALUES (1, 10), (2, 20), (3, 30);'],
        )
        conn = create_db(dataset, 'postgres')
        result = execute_query(conn, 'SELECT * FROM t1 WHERE val > 15', 'postgres')
        conn.close()
        assert result.success
        assert result.has_results
        assert len(result.rows) == 2

    def test_returns_empty(self):
        dataset = _make_dataset(
            ['CREATE TABLE t1 (id INT PRIMARY KEY, val INT);'],
            ['INSERT INTO t1 (id, val) VALUES (1, 10), (2, 20);'],
        )
        conn = create_db(dataset, 'postgres')
        result = execute_query(conn, 'SELECT * FROM t1 WHERE val > 100', 'postgres')
        conn.close()
        assert result.success
        assert not result.has_results
        assert len(result.rows) == 0

    def test_query_error(self):
        dataset = _make_dataset(
            ['CREATE TABLE t1 (id INT PRIMARY KEY);'],
            ['INSERT INTO t1 (id) VALUES (1);'],
        )
        conn = create_db(dataset, 'postgres')
        result = execute_query(conn, 'SELECT * FROM nonexistent_table', 'postgres')
        conn.close()
        assert not result.success
        assert result.error is not None

    def test_columns_returned(self):
        dataset = _make_dataset(
            ['CREATE TABLE t1 (id INT PRIMARY KEY, name VARCHAR);'],
            ["INSERT INTO t1 (id, name) VALUES (1, 'Alice');"],
        )
        conn = create_db(dataset, 'postgres')
        result = execute_query(conn, 'SELECT id, name FROM t1', 'postgres')
        conn.close()
        assert result.columns == ['id', 'name']


# =================================================================
# EXECUTION RESULT
# =================================================================

class TestExecutionResult:

    def test_has_results_true(self):
        r = ExecutionResult(rows=[(1,)], columns=['id'])
        assert r.has_results
        assert r.success

    def test_has_results_false_empty(self):
        r = ExecutionResult(rows=[], columns=[])
        assert not r.has_results
        assert r.success

    def test_has_results_false_error(self):
        r = ExecutionResult(rows=[], columns=[], error='some error')
        assert not r.has_results
        assert not r.success


# =================================================================
# VALIDATE ASSIGNMENT
# =================================================================

class TestValidateAssignment:

    def test_all_exercises_return_results(self):
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
        results = validate_assignment(assignment, 'postgres')
        assert len(results) == 1
        _, result = results[0]
        assert result.has_results

    def test_exercise_returns_no_results(self):
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
        results = validate_assignment(assignment, 'postgres')
        assert len(results) == 1
        _, result = results[0]
        assert result.success
        assert not result.has_results

    def test_multiple_exercises_mixed(self):
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
        results = validate_assignment(assignment, 'postgres')
        assert len(results) == 2
        assert results[0][1].has_results
        assert not results[1][1].has_results
