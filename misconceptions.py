from enum import Enum

import util


class MisconceptionDetails:
    def __init__(self, id: int, description: str, context: str = '', requirements: list[str] = []):
        self.id = id
        self._description = description
        self._context = context
        self._requirements = requirements

    @property
    def description(self) -> str:
        return util.strip_lines(self._description)

    @property
    def context(self) -> str:
        return util.strip_lines(self._context)
    
    @property
    def requirements(self) -> list[str]:
        return [util.strip_lines(req) for req in self._requirements]


class Misconceptions(Enum):
    SYN_1_AMBIGUOUS_DATABASE_OBJECT_OMITTING_CORRELATION_NAMES = MisconceptionDetails(
        id=1,
        description='Omitting correlation names in queries with ambiguous database objects',
    )

    SYN_1_AMBIGUOUS_DATABASE_OBJECT_AMBIGUOUS_COLUMN = MisconceptionDetails(
        id=2,
        description='Ambiguous column without clear correlation',
    )

    SYN_1_AMBIGUOUS_DATABASE_OBJECT_AMBIGUOUS_FUNCTION = MisconceptionDetails(
        id=3,
        description='Ambiguous function reference due to multiple matches',
    )

    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_COLUMN = MisconceptionDetails(
        id=4,
        description='Reference to an undefined column in the database',
    )

    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_FUNCTION = MisconceptionDetails(
        id=5,
        description='Reference to an undefined function',
    )

    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_PARAMETER = MisconceptionDetails(
        id=6,
        description='Undefined parameter used in the query',
    )

    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_OBJECT = MisconceptionDetails(
        id=7,
        description='General undefined object in query context',
    )

    SYN_2_UNDEFINED_DATABASE_OBJECT_INVALID_SCHEMA_NAME = MisconceptionDetails(
        id=8,
        description='Invalid schema name specified',
    )

    SYN_2_UNDEFINED_DATABASE_OBJECT_MISSPELLINGS = MisconceptionDetails(
        id=9,
        description='Misspellings in database object names',
    )

    SYN_2_UNDEFINED_DATABASE_OBJECT_SYNONYMS = MisconceptionDetails(
        id=10,
        description='Usage of synonyms instead of correct object names',
    )

    SYN_2_UNDEFINED_DATABASE_OBJECT_OMITTING_QUOTES_AROUND_CHARACTER_DATA = MisconceptionDetails(
        id=11,
        description='Omitting quotes around character data',
    )
    
    SYN_3_DATA_TYPE_MISMATCH_FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE = MisconceptionDetails(
        id=12,
        description='Failure to specify column name twice where required',
    )
    
    SYN_3_DATA_TYPE_MISMATCH = MisconceptionDetails(
        id=13,
        description='Mismatch between data types in query expressions',
    )
    
    SYN_4_ILLEGAL_AGGREGATE_FUNCTION_PLACEMENT_USING_AGGREGATE_FUNCTION_OUTSIDE_SELECT_OR_HAVING = MisconceptionDetails(
        id=14,
        description='Using aggregate functions outside SELECT or HAVING clauses',
    )
    
    SYN_4_ILLEGAL_AGGREGATE_FUNCTION_PLACEMENT_GROUPING_ERROR_AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED = MisconceptionDetails(
        id=15,
        description='Nesting aggregate functions where not allowed',
    )
    
    SYN_5_ILLEGAL_OR_INSUFFICIENT_GROUPING_GROUPING_ERROR_EXTRANEOUS_OR_OMITTED_GROUPING_COLUMN = MisconceptionDetails(
        id=16,
        description='Grouping error due to extraneous or omitted grouping column',
    )
    
    SYN_5_ILLEGAL_OR_INSUFFICIENT_GROUPING_STRANGE_HAVING_HAVING_WITHOUT_GROUP_BY = MisconceptionDetails(
        id=17,
        description='HAVING clause used without corresponding GROUP BY',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_FUNCTION_WITH_FUNCTION_PARAMETER = MisconceptionDetails(
        id=18,
        description='Confusing function name with function parameter',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_USING_WHERE_TWICE = MisconceptionDetails(
        id=19,
        description='Duplicate WHERE clause used',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_OMITTING_THE_FROM_CLAUSE = MisconceptionDetails(
        id=20,
        description='Omitting the FROM clause in a query',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_COMPARISON_WITH_NULL = MisconceptionDetails(
        id=21,
        description='Improper comparison with NULL',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_OMITTING_THE_SEMICOLON = MisconceptionDetails(
        id=22,
        description='Omitting semicolon at end of statement',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_DATE_TIME_FIELD_OVERFLOW = MisconceptionDetails(
        id=23,
        description='Date/time value overflow in query',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_DUPLICATE_CLAUSE = MisconceptionDetails(
        id=24,
        description='Duplicate clause within the same query',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_USING_AN_UNDEFINED_CORRELATION_NAME = MisconceptionDetails(
        id=25,
        description='Using an undefined correlation name',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_TOO_MANY_COLUMNS_IN_SUBQUERY = MisconceptionDetails(
        id=26,
        description='Excessive columns in a subquery result',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_TABLE_NAMES_WITH_COLUMN_NAMES = MisconceptionDetails(
        id=27,
        description='Confusing table names with column names',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_RESTRICTION_IN_SELECT_CLAUSE = MisconceptionDetails(
        id=28,
        description='Restriction added within the SELECT clause',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_PROJECTION_IN_WHERE_CLAUSE = MisconceptionDetails(
        id=29,
        description='Projection used in the WHERE clause',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_THE_ORDER_OF_KEYWORDS = MisconceptionDetails(
        id=30,
        description='Incorrect order of SQL keywords',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_THE_LOGIC_OF_KEYWORDS = MisconceptionDetails(
        id=31,
        description='Confusing logical functions of keywords',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_THE_SYNTAX_OF_KEYWORDS = MisconceptionDetails(
        id=32,
        description='Syntax confusion in SQL keywords',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_OMITTING_COMMAS = MisconceptionDetails(
        id=33,
        description='Omitting commas between elements',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_CURLY_SQUARE_OR_UNMATCHED_BRACKETS = MisconceptionDetails(
        id=34,
        description='Unmatched or inappropriate brackets',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_IS_WHERE_NOT_APPLICABLE = MisconceptionDetails(
        id=35,
        description='Using IS in an incorrect context',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_NONSTANDARD_KEYWORDS_OR_STANDARD_KEYWORDS_IN_WRONG_CONTEXT = MisconceptionDetails(
        id=36,
        description='Nonstandard or misused keywords',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_NONSTANDARD_OPERATORS = MisconceptionDetails(
        id=37,
        description='Use of nonstandard operators',
    )
    
    SYN_6_COMMON_SYNTAX_ERROR_ADDITIONAL_SEMICOLON = MisconceptionDetails(
        id=38,
        description='Additional semicolon in query',
    )
    
    SEM_1_INCONSISTENT_EXPRESSION_AND_INSTEAD_OF_OR = MisconceptionDetails(
        id=39,
        description='Inconsistent expression: using AND instead of OR',
    )

    SEM_1_INCONSISTENT_EXPRESSION_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION = MisconceptionDetails(
        id=40,
        description='Inconsistent or tautological expression',
        context='Tautological expressions are expressions that always evaluate to TRUE; inconsistent expressions are expressions that always evaluate to FALSE',
    )

    SEM_1_INCONSISTENT_EXPRESSION_DISTINCT_IN_SUM_OR_AVG = MisconceptionDetails(
        id=41,
        description='using DISTINCT used inside SUM or AVG to remove duplicate values outside of the aggregation',
        # context='''
        #     Some users incorrectly assume that using DISTINCT inside SUM or AVG functions will calculate the total or average of all unique values across rows, ignoring duplicates in the entire column regardless of the context. In reality, DISTINCT applies to the subset of values passed to the aggregation function, and its scope is limited to ensuring that duplicates are excluded within the calculation process for the specific aggregation.
        #     SUM(DISTINCT column): Users often expect SUM(column) and SUM(DISTINCT column) to produce similar results, but the latter can be significantly lower if the column contains many duplicates.
        #     AVG(DISTINCT column): This differs from AVG(column), which includes all values, even duplicates.
        #     A common mistake is to believe that SUM(DISTINCT) or AVG(DISTINCT) aggregates values across all rows but somehow retains duplicates outside the context of the calculation. This is incorrect because DISTINCT filters only the specific values passed to the aggregation function.
        #     As an example, an assignment for this misconception might ask students to calculate the total amount spent by each customer on unique products they have ordered.
        
        # ''',
        requirements=[
            # 'Correct query should not include DISTINCT inside SUM or AVG',
            'Using DISTINCT inside SUM or AVG should produce the wrong result',
            # 'Correct query should include DISTINCT outside SUM or AVG; wrong query should include DISTINCT inside SUM or AVG',
            # 'Query should preferibly use only use one of SUM or AVG',
        ],
    )

    SEM_1_INCONSISTENT_EXPRESSION_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES = MisconceptionDetails(
        id=42,
        description='DISTINCT usage potentially removing important duplicates',
    )

    SEM_1_INCONSISTENT_EXPRESSION_WILDCARDS_WITHOUT_LIKE = MisconceptionDetails(
        id=43,
        description='Wildcards used without LIKE',
    )

    SEM_1_INCONSISTENT_EXPRESSION_INCORRECT_WILDCARD_USING_UNDERSCORE_INSTEAD_OF_PERCENT = MisconceptionDetails(
        id=44,
        description='Incorrect wildcard: underscore instead of percent sign',
    )

    SEM_1_INCONSISTENT_EXPRESSION_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL = MisconceptionDetails(
        id=45,
        description='Mixing "> 0" with "IS NOT NULL"',
    )

    SEM_2_INCONSISTENT_JOIN_NULL_IN_SUBQUERY = MisconceptionDetails(
        id=46,
        description='NULL used improperly in subquery',
    )

    SEM_2_INCONSISTENT_JOIN_JOIN_ON_INCORRECT_COLUMN = MisconceptionDetails(
        id=47,
        description='Joining on an incorrect column',
    )

    SEM_3_MISSING_JOIN_OMITTING_A_JOIN = MisconceptionDetails(
        id=48,
        description='Omitted join leading to missing data',
    )

    SEM_4_DUPLICATE_ROWS_MANY_DUPLICATES = MisconceptionDetails(
        id=49,
        description='Duplicate rows where they are not necessary',
    )

    SEM_5_REDUNDANT_COLUMN_OUTPUT_CONSTANT_COLUMN_OUTPUT = MisconceptionDetails(
        id=50,
        description='Output includes redundant constant column',
    )

    SEM_5_REDUNDANT_COLUMN_OUTPUT_DUPLICATE_COLUMN_OUTPUT = MisconceptionDetails(
        id=51,
        description='Duplicate columns in output',
    )

    LOG_1_OPERATOR_ERROR_OR_INSTEAD_OF_AND = MisconceptionDetails(
        id=52,
        description='Using OR instead of AND, affecting result accuracy',
    )

    LOG_1_OPERATOR_ERROR_EXTRANEOUS_NOT_OPERATOR = MisconceptionDetails(
        id=53,
        description='Unnecessary NOT operator',
    )

    LOG_1_OPERATOR_ERROR_MISSING_NOT_OPERATOR = MisconceptionDetails(
        id=54,
        description='Missing NOT operator where required',
    )

    LOG_1_OPERATOR_ERROR_SUBSTITUTING_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO = MisconceptionDetails(
        id=55,
        description='Incorrect existence negation substitution',
    )

    LOG_1_OPERATOR_ERROR_PUTTING_NOT_IN_FRONT_OF_INCORRECT_IN_OR_EXISTS = MisconceptionDetails(
        id=56,
        description='Incorrect use of NOT with IN or EXISTS',
    )

    LOG_1_OPERATOR_ERROR_INCORRECT_COMPARISON_OPERATOR_OR_VALUE = MisconceptionDetails(
        id=57,
        description='Incorrect comparison operator or value',
    )

    LOG_2_JOIN_ERROR_JOIN_ON_INCORRECT_TABLE = MisconceptionDetails(
        id=58,
        description='Joining on incorrect table',
    )

    LOG_2_JOIN_ERROR_JOIN_WHEN_JOIN_NEEDS_TO_BE_OMITTED = MisconceptionDetails(
        id=59,
        description='Unnecessary join that should be omitted',
    )

    LOG_2_JOIN_ERROR_JOIN_ON_INCORRECT_COLUMN_MATCHES_POSSIBLE = MisconceptionDetails(
        id=60,
        description='Incorrect join column with possible matches',
    )

    LOG_2_JOIN_ERROR_JOIN_WITH_INCORRECT_COMPARISON_OPERATOR = MisconceptionDetails(
        id=61,
        description='Using incorrect comparison operator in join',
    )

    LOG_2_JOIN_ERROR_MISSING_JOIN = MisconceptionDetails(
        id=62,
        description='Missing join where required for result accuracy',
    )

    LOG_3_NESTING_ERROR_IMPROPER_NESTING_OF_EXPRESSIONS = MisconceptionDetails(
        id=63,
        description='Improper nesting of expressions in conditions',
    )

    LOG_3_NESTING_ERROR_IMPROPER_NESTING_OF_SUBQUERIES = MisconceptionDetails(
        id=64,
        description='Incorrect subquery nesting',
    )

    LOG_4_EXPRESSION_ERROR_EXTRANEOUS_QUOTES = MisconceptionDetails(
        id=65,
        description='Unnecessary quotes in expressions',
    )

    LOG_4_EXPRESSION_ERROR_MISSING_EXPRESSION = MisconceptionDetails(
        id=66,
        description='Expected expression missing in query',
    )

    LOG_4_EXPRESSION_ERROR_EXPRESSION_ON_INCORRECT_COLUMN = MisconceptionDetails(
        id=67,
        description='Expression used on an incorrect column',
    )

    LOG_4_EXPRESSION_ERROR_EXTRANEOUS_EXPRESSION = MisconceptionDetails(
        id=68,
        description='Superfluous expression included',
    )

    LOG_4_EXPRESSION_ERROR_EXPRESSION_IN_INCORRECT_CLAUSE = MisconceptionDetails(
        id=69,
        description='Expression used in incorrect clause',
    )

    LOG_5_PROJECTION_ERROR_EXTRANEOUS_COLUMN_IN_SELECT = MisconceptionDetails(
        id=70,
        description='Extraneous column included in SELECT clause',
    )

    LOG_5_PROJECTION_ERROR_MISSING_COLUMN_FROM_SELECT = MisconceptionDetails(
        id=71,
        description='Expected column missing from SELECT clause',
    )

    LOG_5_PROJECTION_ERROR_MISSING_DISTINCT_FROM_SELECT = MisconceptionDetails(
        id=72,
        description='Missing DISTINCT keyword in SELECT clause',
    )

    LOG_5_PROJECTION_ERROR_MISSING_AS_FROM_SELECT = MisconceptionDetails(
        id=73,
        description='Missing AS keyword for column alias in SELECT',
    )

    LOG_5_PROJECTION_ERROR_MISSING_COLUMN_FROM_ORDER_BY = MisconceptionDetails(
        id=74,
        description='Expected column missing from ORDER BY clause',
    )

    LOG_5_PROJECTION_ERROR_INCORRECT_COLUMN_IN_ORDER_BY = MisconceptionDetails(
        id=75,
        description='Incorrect column used in ORDER BY clause',
    )

    LOG_5_PROJECTION_ERROR_EXTRANEOUS_ORDER_BY_CLAUSE = MisconceptionDetails(
        id=76,
        description='Unnecessary ORDER BY clause used',
    )

    LOG_5_PROJECTION_ERROR_INCORRECT_ORDERING_OF_ROWS = MisconceptionDetails(
        id=77,
        description='Incorrect row ordering in query result',
    )

    LOG_6_FUNCTION_ERROR_DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE = MisconceptionDetails(
        id=78,
        description='DISTINCT used as a function parameter unnecessarily',
    )

    LOG_6_FUNCTION_ERROR_MISSING_DISTINCT_FROM_FUNCTION_PARAMETER = MisconceptionDetails(
        id=79,
        description='DISTINCT omitted as function parameter when required',
    )

    LOG_6_FUNCTION_ERROR_INCORRECT_FUNCTION = MisconceptionDetails(
        id=80,
        description='Incorrect function used for the given data demand',
    )

    LOG_6_FUNCTION_ERROR_INCORRECT_COLUMN_AS_FUNCTION_PARAMETER = MisconceptionDetails(
        id=81,
        description='Incorrect column used as function parameter',
    )

    COM_1_COMPLICATION_UNNECESSARY_COMPLICATION = MisconceptionDetails(
        id=82,
        description='Query is unnecessarily complicated',
    )

    COM_1_COMPLICATION_UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE = MisconceptionDetails(
        id=83,
        description='Unnecessary DISTINCT keyword in SELECT clause',
    )

    COM_1_COMPLICATION_UNNECESSARY_JOIN = MisconceptionDetails(
        id=84,
        description='Unnecessary join operation',
    )

    COM_1_COMPLICATION_UNUSED_CORRELATION_NAME = MisconceptionDetails(
        id=85,
        description='Correlation name defined but never used',
    )

    COM_1_COMPLICATION_CORRELATION_NAMES_ARE_ALWAYS_IDENTICAL = MisconceptionDetails(
        id=86,
        description='Identical correlation names used unnecessarily',
    )

    COM_1_COMPLICATION_UNNECESSARILY_GENERAL_COMPARISON_OPERATOR = MisconceptionDetails(
        id=87,
        description='Overly general comparison operator used',
    )

    COM_1_COMPLICATION_LIKE_WITHOUT_WILDCARDS = MisconceptionDetails(
        id=88,
        description='LIKE operator used without wildcards',
    )

    COM_1_COMPLICATION_UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY = MisconceptionDetails(
        id=89,
        description='SELECT clause in EXISTS subquery is overly complicated',
    )

    COM_1_COMPLICATION_IN_EXISTS_CAN_BE_REPLACED_BY_COMPARISON = MisconceptionDetails(
        id=90,
        description='IN/EXISTS subquery could be replaced by a simple comparison',
    )

    COM_1_COMPLICATION_UNNECESSARY_AGGREGATE_FUNCTION = MisconceptionDetails(
        id=91,
        description='Unnecessary aggregate function used in query',
    )

    COM_1_COMPLICATION_UNNECESSARY_DISTINCT_IN_AGGREGATE_FUNCTION = MisconceptionDetails(
        id=92,
        description='DISTINCT unnecessarily used in aggregate function',
    )

    COM_1_COMPLICATION_UNNECESSARY_ARGUMENT_OF_COUNT = MisconceptionDetails(
        id=93,
        description='COUNT function includes unnecessary argument',
    )

    COM_1_COMPLICATION_UNNECESSARY_GROUP_BY_IN_EXISTS_SUBQUERY = MisconceptionDetails(
        id=94,
        description='GROUP BY clause used unnecessarily in EXISTS subquery',
    )

    COM_1_COMPLICATION_GROUP_BY_WITH_SINGLETON_GROUPS = MisconceptionDetails(
        id=95,
        description='GROUP BY clause creates singleton groups unnecessarily',
    )

    COM_1_COMPLICATION_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT = MisconceptionDetails(
        id=96,
        description='GROUP BY clause could be replaced by DISTINCT',
    )

    COM_1_COMPLICATION_UNION_CAN_BE_REPLACED_BY_OR = MisconceptionDetails(
        id=97,
        description='UNION operation could be replaced by OR condition',
    )

    COM_1_COMPLICATION_UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE = MisconceptionDetails(
        id=99,
        description='Unnecessary column specified in ORDER BY clause',
    )

    COM_1_COMPLICATION_ORDER_BY_IN_SUBQUERY = MisconceptionDetails(
        id=100,
        description='ORDER BY clause used in subquery unnecessarily',
    )

    COM_1_COMPLICATION_INEFFICIENT_HAVING = MisconceptionDetails(
        id=101,
        description='Inefficient HAVING clause',
    )

    COM_1_COMPLICATION_INEFFICIENT_UNION = MisconceptionDetails(
        id=102,
        description='Inefficient use of UNION operation',
    )

    COM_1_COMPLICATION_CONDITION_IN_SUBQUERY_CAN_BE_MOVED_UP = MisconceptionDetails(
        id=103,
        description='Condition in subquery could be moved up for efficiency',
    )

    COM_1_COMPLICATION_CONDITION_ON_LEFT_TABLE_IN_LEFT_OUTER_JOIN = MisconceptionDetails(
        id=104,
        description='Condition applied to left table in LEFT OUTER JOIN unnecessarily',
    )

    COM_1_COMPLICATION_OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN = MisconceptionDetails(
        id=105,
        description='Outer join used when inner join would suffice',
    )

    COM_X_COMPLICATION_JOIN_CONDITION_IN_WHERE_CLAUSE = MisconceptionDetails(
        id=106,
        description='Join condition specified in WHERE clause instead of ON clause',
    )

