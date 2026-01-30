import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.aggregation import NoAggregation, Aggregation
from sql_assignment_generator.exceptions import ConstraintValidationError


def test_no_aggregation_fail():
    sql = "SELECT department, COUNT(*) FROM employees GROUP BY department;"
    query = Query(sql)

    constraint = NoAggregation()

    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

def test_no_aggregation_pass():
    sql = "SELECT name, age FROM employees WHERE age > 30;"
    query = Query(sql)

    constraint = NoAggregation()

    # Should not raise any exception
    constraint.validate(query)

def test_aggregation_fail():
    sql = "SELECT name, age FROM employees WHERE age > 30;"
    query = Query(sql)

    constraint = Aggregation()

    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

def test_aggregation_pass():
    sql = "SELECT department, SUM(salary) FROM employees GROUP BY department;"
    query = Query(sql)

    constraint = Aggregation()

    # Should not raise any exception
    constraint.validate(query)