from enum import Enum
import random
import time

import util


class SQLErrorDetails:
    def __init__(self, id: int, description: str, requirements: list[str] = []):
        self.id = id
        self._description = description
        self._requirements = requirements

    @property
    def description(self) -> str:
        return util.strip_lines(self._description)

    @property
    def requirements(self) -> list[str]:
        # set seed to ensure requirements are generated consintently during program execution
        random.seed(self._rseed)

        reqs = []

        for req in self._requirements:
            if isinstance(req, list):
                req = random.choice(req)        # take a random requirement from a list

            reqs.append(util.strip_lines(req))

        return reqs


class Misconceptions(Enum):
    # TODO SYN 1
    SYN_1_AMBIGUOUS_DATABASE_OBJECT_OMITTING_CORRELATION_NAMES = SQLErrorDetails(
        id=1,
        description='Omitting correlation names in queries with ambiguous database objects',
    )

    # TODO SYN 2
    SYN_1_AMBIGUOUS_DATABASE_OBJECT_AMBIGUOUS_COLUMN = SQLErrorDetails(
        id=2,
        description='Ambiguous column without clear correlation',
    )

    # TODO SYN 3
    SYN_1_AMBIGUOUS_DATABASE_OBJECT_AMBIGUOUS_FUNCTION = SQLErrorDetails(
        id=3,
        description='Ambiguous function reference due to multiple matches',
    )

    # TODO SYN 4
    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_COLUMN = SQLErrorDetails(
        id=4,
        description='Reference to an undefined column in the database',
    )

    # TODO SYN 5
    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_FUNCTION = SQLErrorDetails(
        id=5,
        description='Reference to an undefined function',
    )

    # TODO SYN 6
    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_PARAMETER = SQLErrorDetails(
        id=6,
        description='Undefined parameter used in the query',
    )

    # TODO SYN 7
    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_OBJECT = SQLErrorDetails(
        id=7,
        description='General undefined object in query context',
    )

    # TODO SYN 8
    SYN_2_UNDEFINED_DATABASE_OBJECT_INVALID_SCHEMA_NAME = SQLErrorDetails(
        id=8,
        description='Invalid schema name specified',
    )

    # TODO SYN 9
    SYN_2_UNDEFINED_DATABASE_OBJECT_MISSPELLINGS = SQLErrorDetails(
        id=9,
        description='Misspellings in database object names',
    )

    # TODO SYN 10
    SYN_2_UNDEFINED_DATABASE_OBJECT_SYNONYMS = SQLErrorDetails(
        id=10,
        description='Usage of synonyms instead of correct object names',
    )

    # TODO SYN 11
    SYN_2_UNDEFINED_DATABASE_OBJECT_OMITTING_QUOTES_AROUND_CHARACTER_DATA = SQLErrorDetails(
        id=11,
        description='Omitting quotes around character data',
    )
    
    # TODO SYN 12
    SYN_3_DATA_TYPE_MISMATCH_FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE = SQLErrorDetails(
        id=12,
        description='Failure to specify column name twice where required',
    )
    
    # TODO SYN 13
    SYN_3_DATA_TYPE_MISMATCH = SQLErrorDetails(
        id=13,
        description='Mismatch between data types in query expressions',
    )
    
    # TODO SYN 14
    SYN_4_ILLEGAL_AGGREGATE_FUNCTION_PLACEMENT_USING_AGGREGATE_FUNCTION_OUTSIDE_SELECT_OR_HAVING = SQLErrorDetails(
        id=14,
        description='Using aggregate functions outside SELECT or HAVING clauses',
    )
    
    # TODO SYN 15
    SYN_4_ILLEGAL_AGGREGATE_FUNCTION_PLACEMENT_GROUPING_ERROR_AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED = SQLErrorDetails(
        id=15,
        description='Nesting aggregate functions where not allowed',
    )
    
    # TODO SYN 16
    SYN_5_ILLEGAL_OR_INSUFFICIENT_GROUPING_GROUPING_ERROR_EXTRANEOUS_OR_OMITTED_GROUPING_COLUMN = SQLErrorDetails(
        id=16,
        description='Grouping error due to extraneous or omitted grouping column',
    )
    
    # TODO SYN 17
    SYN_5_ILLEGAL_OR_INSUFFICIENT_GROUPING_STRANGE_HAVING_HAVING_WITHOUT_GROUP_BY = SQLErrorDetails(
        id=17,
        description='HAVING clause used without corresponding GROUP BY',
    )
    
    # TODO SYN 18
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_FUNCTION_WITH_FUNCTION_PARAMETER = SQLErrorDetails(
        id=18,
        description='Confusing function name with function parameter',
    )
    
    # TODO SYN 19
    SYN_6_COMMON_SYNTAX_ERROR_USING_WHERE_TWICE = SQLErrorDetails(
        id=19,
        description='Duplicate WHERE clause used',
    )
    
    # TODO SYN 20
    SYN_6_COMMON_SYNTAX_ERROR_OMITTING_THE_FROM_CLAUSE = SQLErrorDetails(
        id=20,
        description='Omitting the FROM clause in a query',
    )
    
    # TODO SYN 21
    SYN_6_COMMON_SYNTAX_ERROR_COMPARISON_WITH_NULL = SQLErrorDetails(
        id=21,
        description='Improper comparison with NULL',
    )
    
    # TODO SYN 22
    SYN_6_COMMON_SYNTAX_ERROR_OMITTING_THE_SEMICOLON = SQLErrorDetails(
        id=22,
        description='Omitting semicolon at end of statement',
    )
    
    # TODO SYN 23
    SYN_6_COMMON_SYNTAX_ERROR_DATE_TIME_FIELD_OVERFLOW = SQLErrorDetails(
        id=23,
        description='Date/time value overflow in query',
    )
    
    # TODO SYN 24
    SYN_6_COMMON_SYNTAX_ERROR_DUPLICATE_CLAUSE = SQLErrorDetails(
        id=24,
        description='Duplicate clause within the same query',
    )
    
    # TODO SYN 25
    SYN_6_COMMON_SYNTAX_ERROR_USING_AN_UNDEFINED_CORRELATION_NAME = SQLErrorDetails(
        id=25,
        description='Using an undefined correlation name',
    )
    
    # TODO SYN 26
    SYN_6_COMMON_SYNTAX_ERROR_TOO_MANY_COLUMNS_IN_SUBQUERY = SQLErrorDetails(
        id=26,
        description='Excessive columns in a subquery result',
    )
    
    # TODO SYN 27
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_TABLE_NAMES_WITH_COLUMN_NAMES = SQLErrorDetails(
        id=27,
        description='Confusing table names with column names',
    )
    
    # TODO SYN 28
    SYN_6_COMMON_SYNTAX_ERROR_RESTRICTION_IN_SELECT_CLAUSE = SQLErrorDetails(
        id=28,
        description='Restriction added within the SELECT clause',
    )
    
    # TODO SYN 29
    SYN_6_COMMON_SYNTAX_ERROR_PROJECTION_IN_WHERE_CLAUSE = SQLErrorDetails(
        id=29,
        description='Projection used in the WHERE clause',
    )
    
    # TODO SYN 30
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_THE_ORDER_OF_KEYWORDS = SQLErrorDetails(
        id=30,
        description='Incorrect order of SQL keywords',
    )
    
    # TODO SYN 31
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_THE_LOGIC_OF_KEYWORDS = SQLErrorDetails(
        id=31,
        description='Confusing logical functions of keywords',
    )
    
    # TODO SYN 32
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_THE_SYNTAX_OF_KEYWORDS = SQLErrorDetails(
        id=32,
        description='Syntax confusion in SQL keywords',
    )
    
    # TODO SYN 33
    SYN_6_COMMON_SYNTAX_ERROR_OMITTING_COMMAS = SQLErrorDetails(
        id=33,
        description='Omitting commas between elements',
    )
    
    # TODO SYN 34
    SYN_6_COMMON_SYNTAX_ERROR_CURLY_SQUARE_OR_UNMATCHED_BRACKETS = SQLErrorDetails(
        id=34,
        description='Unmatched or inappropriate brackets',
    )
    
    # TODO SYN 35
    SYN_6_COMMON_SYNTAX_ERROR_IS_WHERE_NOT_APPLICABLE = SQLErrorDetails(
        id=35,
        description='Using IS in an incorrect context',
    )
    
    # TODO SYN 36
    SYN_6_COMMON_SYNTAX_ERROR_NONSTANDARD_KEYWORDS_OR_STANDARD_KEYWORDS_IN_WRONG_CONTEXT = SQLErrorDetails(
        id=36,
        description='Nonstandard or misused keywords',
    )
    
    # TODO SYN 37
    SYN_6_COMMON_SYNTAX_ERROR_NONSTANDARD_OPERATORS = SQLErrorDetails(
        id=37,
        description='Use of nonstandard operators',
    )
    
    # TODO SYN 38
    SYN_6_COMMON_SYNTAX_ERROR_ADDITIONAL_SEMICOLON = SQLErrorDetails(
        id=38,
        description='Additional semicolon in query',
    )
    
    SEM_1_INCONSISTENT_EXPRESSION_AND_INSTEAD_OF_OR = SQLErrorDetails(
        id=39,
        description='erroneosly using AND instead of OR',
        requirements=[
            'Use two conditions on the same attribute, connected by OR',    # without this, we usually get conditions on two different attributes 
            'Formulate the request so that students could be mislead into using AND instead of OR',
        ]
    )

    # FIXME SEM 40 does not work 
    SEM_1_INCONSISTENT_EXPRESSION_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION = SQLErrorDetails(
        id=40,
        description='writing tautological or inconsistent expressions',
        requirements=[
            [
                'The assignment must contain a request which could lead students into writing a condition that seems meaningful to solving the request but actually always evaluates to TRUE.',
                'The assignment must contain a request which could lead students into writing a condition that seems meaningful to solving the request but actually always evaluates to FALSE.',
                # 'The assignment must contain a request which could trick students into writing a part of a condition which is logically contained within another part (e.g. x>500 OR x>700: in this case x>700 is contained within x>500)',
                # 'The assignment must contain a request which could trick students into writing a part of a condition which is made not necessary by another part (e.g. (x < 5 AND y > 10) OR x >= 5: in this case the condition can be replaced with y>10 OR x >= 5)',
            ],
        ],
    )

    SEM_1_INCONSISTENT_EXPRESSION_DISTINCT_IN_SUM_OR_AVG = SQLErrorDetails(
        id=41,
        description='using DISTINCT inside SUM or AVG to remove duplicate values outside of the aggregation',
        requirements=[
            [
                'Using DISTINCT inside SUM should produce the wrong result',
                'Using DISTINCT inside AVG should produce the wrong result',
            ],
        ],
    )

    SEM_1_INCONSISTENT_EXPRESSION_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES = SQLErrorDetails(
        id=42,
        description='using DISTINCT or GROUP BY might remove important duplicates',
        requirements=[
            'The query should list all values of a column which can have duplicate names',  # without this, queries usually ask for ids. Names help keeping the query practical
            'The query should require some filtering conditions',   # helps keeping the query interesting, otherwise we just get a plain SELECT ... FROM ...
            [
                'Using DISTINCT should produce the wrong result. The correct solution should not use DISTINCT',
                'Using GROUP BY should produce the wrong result. The correct solution should not use GROUP BY',
            ],
        ],
    )

    SEM_1_INCONSISTENT_EXPRESSION_WILDCARDS_WITHOUT_LIKE = SQLErrorDetails(
        id=43,
        description='Wildcards used without LIKE',
    )

    SEM_1_INCONSISTENT_EXPRESSION_INCORRECT_WILDCARD_USING_UNDERSCORE_INSTEAD_OF_PERCENT = SQLErrorDetails(
        id=44,
        description='Incorrect wildcard: "_" instead of "%" or using not supported characters, e.g. "*"',
        requirements=[
            [
                'Wildcard requires at least one "%"',
                'Wildcard requires at least one "_"',
                'Wildcard requires at least one "%" and at least one "_"',
            ]
        ]
    )

    # TODO SEM 45
    SEM_1_INCONSISTENT_EXPRESSION_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL = SQLErrorDetails(
        id=45,
        description='Mixing "> 0" with "IS NOT NULL"',
    )

    # TODO SEM 46
    SEM_2_INCONSISTENT_JOIN_NULL_IN_IN_ANY_ALL_SUBQUERY = SQLErrorDetails(
        id=46,
        description='NULL values present in IN/ANY/ALL subquery',
        requirements=[
            'The subquery can evaluate to NULL',
            'The subquery has a simple condition',
            [
                'The WHERE condition in the main query uses IN (...)',
                'The WHERE condition in the main query uses ANY (...)',
                'The WHERE condition in the main query uses ALL (...)',
            ]
        ],
    )

    # TODO SEM 47
    SEM_2_INCONSISTENT_JOIN_JOIN_ON_INCORRECT_COLUMN = SQLErrorDetails(
        id=47,
        description='Joining on an incorrect column',
    )

    # TODO SEM 48
    SEM_3_MISSING_JOIN_OMITTING_A_JOIN = SQLErrorDetails(
        id=48,
        description='Omitted join leading to missing data',
    )

    # TODO SEM 49
    SEM_4_DUPLICATE_ROWS_MANY_DUPLICATES = SQLErrorDetails(
        id=49,
        description='Duplicate rows where they are not necessary',
    )

    # TODO SEM 50
    SEM_5_REDUNDANT_COLUMN_OUTPUT_CONSTANT_COLUMN_OUTPUT = SQLErrorDetails(
        id=50,
        description='Output includes redundant constant column',
    )

    # TODO SEM 51
    SEM_5_REDUNDANT_COLUMN_OUTPUT_DUPLICATE_COLUMN_OUTPUT = SQLErrorDetails(
        id=51,
        description='Duplicate columns in output',
    )

    # TODO LOG 52
    LOG_1_OPERATOR_ERROR_OR_INSTEAD_OF_AND = SQLErrorDetails(
        id=52,
        description='Using OR instead of AND, affecting result accuracy',
    )

    # TODO LOG 53
    LOG_1_OPERATOR_ERROR_EXTRANEOUS_NOT_OPERATOR = SQLErrorDetails(
        id=53,
        description='Unnecessary NOT operator',
    )

    # TODO LOG 54
    LOG_1_OPERATOR_ERROR_MISSING_NOT_OPERATOR = SQLErrorDetails(
        id=54,
        description='Missing NOT operator where required',
    )

    # TODO LOG 55
    LOG_1_OPERATOR_ERROR_SUBSTITUTING_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO = SQLErrorDetails(
        id=55,
        description='Incorrect existence negation substitution',
    )

    # TODO LOG 56
    LOG_1_OPERATOR_ERROR_PUTTING_NOT_IN_FRONT_OF_INCORRECT_IN_OR_EXISTS = SQLErrorDetails(
        id=56,
        description='Incorrect use of NOT with IN or EXISTS',
    )

    # TODO LOG 57
    LOG_1_OPERATOR_ERROR_INCORRECT_COMPARISON_OPERATOR_OR_VALUE = SQLErrorDetails(
        id=57,
        description='Incorrect comparison operator or value',
    )

    # TODO LOG 58
    LOG_2_JOIN_ERROR_JOIN_ON_INCORRECT_TABLE = SQLErrorDetails(
        id=58,
        description='Joining on incorrect table',
    )

    # TODO LOG 59
    LOG_2_JOIN_ERROR_JOIN_WHEN_JOIN_NEEDS_TO_BE_OMITTED = SQLErrorDetails(
        id=59,
        description='Unnecessary join that should be omitted',
    )

    # TODO LOG 60
    LOG_2_JOIN_ERROR_JOIN_ON_INCORRECT_COLUMN_MATCHES_POSSIBLE = SQLErrorDetails(
        id=60,
        description='Incorrect join column with possible matches',
    )

    # TODO LOG 61
    LOG_2_JOIN_ERROR_JOIN_WITH_INCORRECT_COMPARISON_OPERATOR = SQLErrorDetails(
        id=61,
        description='Using incorrect comparison operator in join',
    )

    # TODO LOG 62
    LOG_2_JOIN_ERROR_MISSING_JOIN = SQLErrorDetails(
        id=62,
        description='Missing join where required for result accuracy',
    )

    # TODO LOG 63
    LOG_3_NESTING_ERROR_IMPROPER_NESTING_OF_EXPRESSIONS = SQLErrorDetails(
        id=63,
        description='Improper nesting of expressions in conditions',
    )

    # TODO LOG 64
    LOG_3_NESTING_ERROR_IMPROPER_NESTING_OF_SUBQUERIES = SQLErrorDetails(
        id=64,
        description='Incorrect subquery nesting',
    )

    # TODO LOG 65
    LOG_4_EXPRESSION_ERROR_EXTRANEOUS_QUOTES = SQLErrorDetails(
        id=65,
        description='Unnecessary quotes in expressions',
    )

    # TODO LOG 66
    LOG_4_EXPRESSION_ERROR_MISSING_EXPRESSION = SQLErrorDetails(
        id=66,
        description='Expected expression missing in query',
    )

    # TODO LOG 67
    LOG_4_EXPRESSION_ERROR_EXPRESSION_ON_INCORRECT_COLUMN = SQLErrorDetails(
        id=67,
        description='Expression used on an incorrect column',
    )

    # TODO LOG 68
    LOG_4_EXPRESSION_ERROR_EXTRANEOUS_EXPRESSION = SQLErrorDetails(
        id=68,
        description='Superfluous expression included',
    )

    # TODO LOG 69
    LOG_4_EXPRESSION_ERROR_EXPRESSION_IN_INCORRECT_CLAUSE = SQLErrorDetails(
        id=69,
        description='Expression used in incorrect clause',
    )

    # TODO LOG 70
    LOG_5_PROJECTION_ERROR_EXTRANEOUS_COLUMN_IN_SELECT = SQLErrorDetails(
        id=70,
        description='Extraneous column included in SELECT clause',
    )

    # TODO LOG 71
    LOG_5_PROJECTION_ERROR_MISSING_COLUMN_FROM_SELECT = SQLErrorDetails(
        id=71,
        description='Expected column missing from SELECT clause',
    )

    # TODO LOG 72
    LOG_5_PROJECTION_ERROR_MISSING_DISTINCT_FROM_SELECT = SQLErrorDetails(
        id=72,
        description='Missing DISTINCT keyword in SELECT clause',
    )

    # TODO LOG 73
    LOG_5_PROJECTION_ERROR_MISSING_AS_FROM_SELECT = SQLErrorDetails(
        id=73,
        description='Missing AS keyword for column alias in SELECT',
    )

    # TODO LOG 74
    LOG_5_PROJECTION_ERROR_MISSING_COLUMN_FROM_ORDER_BY = SQLErrorDetails(
        id=74,
        description='Expected column missing from ORDER BY clause',
    )

    # TODO LOG 75
    LOG_5_PROJECTION_ERROR_INCORRECT_COLUMN_IN_ORDER_BY = SQLErrorDetails(
        id=75,
        description='Incorrect column used in ORDER BY clause',
    )

    # TODO LOG 76
    LOG_5_PROJECTION_ERROR_EXTRANEOUS_ORDER_BY_CLAUSE = SQLErrorDetails(
        id=76,
        description='Unnecessary ORDER BY clause used',
    )

    # TODO LOG 77
    LOG_5_PROJECTION_ERROR_INCORRECT_ORDERING_OF_ROWS = SQLErrorDetails(
        id=77,
        description='Incorrect row ordering in query result',
    )

    # TODO LOG 78
    LOG_6_FUNCTION_ERROR_DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE = SQLErrorDetails(
        id=78,
        description='DISTINCT used as a function parameter unnecessarily',
    )

    # TODO LOG 79
    LOG_6_FUNCTION_ERROR_MISSING_DISTINCT_FROM_FUNCTION_PARAMETER = SQLErrorDetails(
        id=79,
        description='DISTINCT omitted as function parameter when required',
    )

    # TODO LOG 80
    LOG_6_FUNCTION_ERROR_INCORRECT_FUNCTION = SQLErrorDetails(
        id=80,
        description='Incorrect function used for the given data demand',
    )

    # TODO LOG 81
    LOG_6_FUNCTION_ERROR_INCORRECT_COLUMN_AS_FUNCTION_PARAMETER = SQLErrorDetails(
        id=81,
        description='Incorrect column used as function parameter',
    )

    # TODO COM 82
    COM_1_COMPLICATION_UNNECESSARY_COMPLICATION = SQLErrorDetails(
        id=82,
        description='Query is unnecessarily complicated',
    )

    # TODO COM 83
    COM_1_COMPLICATION_UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE = SQLErrorDetails(
        id=83,
        description='Unnecessary DISTINCT keyword in SELECT clause',
    )

    # TODO COM 84
    COM_1_COMPLICATION_UNNECESSARY_JOIN = SQLErrorDetails(
        id=84,
        description='Unnecessary join operation',
    )

    # TODO COM 85
    COM_1_COMPLICATION_UNUSED_CORRELATION_NAME = SQLErrorDetails(
        id=85,
        description='Correlation name defined but never used',
    )

    # TODO COM 86
    COM_1_COMPLICATION_CORRELATION_NAMES_ARE_ALWAYS_IDENTICAL = SQLErrorDetails(
        id=86,
        description='Identical correlation names used unnecessarily',
    )

    # TODO COM 87
    COM_1_COMPLICATION_UNNECESSARILY_GENERAL_COMPARISON_OPERATOR = SQLErrorDetails(
        id=87,
        description='Overly general comparison operator used',
    )

    # TODO COM 88
    COM_1_COMPLICATION_LIKE_WITHOUT_WILDCARDS = SQLErrorDetails(
        id=88,
        description='LIKE operator used without wildcards',
    )

    # TODO COM 89
    COM_1_COMPLICATION_UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY = SQLErrorDetails(
        id=89,
        description='SELECT clause in EXISTS subquery is overly complicated',
    )

    # TODO COM 90
    COM_1_COMPLICATION_IN_EXISTS_CAN_BE_REPLACED_BY_COMPARISON = SQLErrorDetails(
        id=90,
        description='IN/EXISTS subquery could be replaced by a simple comparison',
    )

    # TODO COM 91
    COM_1_COMPLICATION_UNNECESSARY_AGGREGATE_FUNCTION = SQLErrorDetails(
        id=91,
        description='Unnecessary aggregate function used in query',
    )

    # TODO COM 92
    COM_1_COMPLICATION_UNNECESSARY_DISTINCT_IN_AGGREGATE_FUNCTION = SQLErrorDetails(
        id=92,
        description='DISTINCT unnecessarily used in aggregate function',
    )

    # TODO COM 93
    COM_1_COMPLICATION_UNNECESSARY_ARGUMENT_OF_COUNT = SQLErrorDetails(
        id=93,
        description='COUNT function includes unnecessary argument',
    )

    # TODO COM 94
    COM_1_COMPLICATION_UNNECESSARY_GROUP_BY_IN_EXISTS_SUBQUERY = SQLErrorDetails(
        id=94,
        description='GROUP BY clause used unnecessarily in EXISTS subquery',
    )

    # TODO COM 95
    COM_1_COMPLICATION_GROUP_BY_WITH_SINGLETON_GROUPS = SQLErrorDetails(
        id=95,
        description='GROUP BY clause creates singleton groups unnecessarily',
    )

    # TODO COM 96
    COM_1_COMPLICATION_GROUP_BY_WITH_ONLY_A_SINGLE_GROUP = SQLErrorDetails(
        id=96,
        description='using GROUP BY with a single group',
    )

    # TODO COM 97
    COM_1_COMPLICATION_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT = SQLErrorDetails(
        id=97,
        description='GROUP BY clause could be replaced by DISTINCT',
    )

    # TODO COM 98
    COM_1_COMPLICATION_UNION_CAN_BE_REPLACED_BY_OR = SQLErrorDetails(
        id=98,
        description='UNION operation could be replaced by OR condition',
    )

    # TODO COM 99
    COM_1_COMPLICATION_UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE = SQLErrorDetails(
        id=99,
        description='Unnecessary column specified in ORDER BY clause',
    )

    # TODO COM 100
    COM_1_COMPLICATION_ORDER_BY_IN_SUBQUERY = SQLErrorDetails(
        id=100,
        description='ORDER BY clause used in subquery unnecessarily',
    )

    # TODO COM 101
    COM_1_COMPLICATION_INEFFICIENT_HAVING = SQLErrorDetails(
        id=101,
        description='Inefficient HAVING clause',
    )

    # TODO COM 102
    COM_1_COMPLICATION_INEFFICIENT_UNION = SQLErrorDetails(
        id=102,
        description='Inefficient use of UNION operation',
    )

    # TODO COM 103
    COM_1_COMPLICATION_CONDITION_IN_SUBQUERY_CAN_BE_MOVED_UP = SQLErrorDetails(
        id=103,
        description='Condition in subquery could be moved up for efficiency',
    )

    # TODO COM 104
    COM_1_COMPLICATION_CONDITION_ON_LEFT_TABLE_IN_LEFT_OUTER_JOIN = SQLErrorDetails(
        id=104,
        description='Condition applied to left table in LEFT OUTER JOIN unnecessarily',
    )

    # TODO COM 105
    COM_1_COMPLICATION_OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN = SQLErrorDetails(
        id=105,
        description='Outer join used when inner join would suffice',
    )

    # TODO COM 106
    COM_X_COMPLICATION_JOIN_CONDITION_IN_WHERE_CLAUSE = SQLErrorDetails(
        id=106,
        description='Join condition specified in WHERE clause instead of ON clause',
    )

