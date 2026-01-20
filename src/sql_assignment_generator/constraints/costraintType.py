from enum import Enum

class WhereConstraintType(Enum):
    CLASSIC = "WHERE conditions"
    STRING = "WHERE STRING conditions"
    EMPTY = "WHERE EMPTY conditions"
    NULL = "WHERE NULL conditions"
    NOT_NULL = "WHERE NOT NULL conditions"
    MULTIPLE = "MULTIPLE WHERE conditions"
    NESTED = "NESTED WHERE conditions"
    WILDCARD = "WHERE conditions with WILDCARD, use more than 5 letter into WILDCARD"
    NO_WILDCARD = "WHERE conditions without WILDCARD, use more than 5 letter into WILDCARD"
    EXIST = "EXIST in WHERE conditions"
    NOT_EXIST = "NOT EXIST in WHERE conditions"
    EXIST_OR_IN = "EXIST and NOT EXIST or IN and NOT IN into WHERE conditions"
    NOT = "NOT in WHERE conditions"
    COMPARISON_OPERATORS = "COMPARISON OPERATORS in WHERE conditions"
    ANY_ALL_IN = "ANY or ALL or IN in WHERE conditions"
    HAVING = "WHERE or HAVING conditions"


class DistinctOrUKInSelectConstraintType(Enum):
    DISTINCT = "DISTINCT"
    UK = "PRIMARY or UNIQUE KEY in SELECT"
    DISTINCT_UK = "DISTINCT or UNIQUE KEY in SELECT"

class AggregationConstraintType(Enum):
    SUM = "SUM"
    AVG = "AVG"
    COUNT = "COUNT"
    MAX = "MAX"
    MIN = "MIN"
    EXTRACT = "EXTRACT"
    LENGTH = "LENGTH"