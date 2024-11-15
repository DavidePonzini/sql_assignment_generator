from enum import Enum


class MisconceptionDetails:
    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description


class Misconceptions(Enum):
    SYN_1_AMBIGUOUS_DATABASE_OBJECT_OMITTING_CORRELATION_NAMES = MisconceptionDetails(
        1, 'Omitting correlation names in queries with ambiguous database objects'
    )
    SYN_1_AMBIGUOUS_DATABASE_OBJECT_AMBIGUOUS_COLUMN = MisconceptionDetails(
        2, 'Ambiguous column without clear correlation'
    )
    SYN_1_AMBIGUOUS_DATABASE_OBJECT_AMBIGUOUS_FUNCTION = MisconceptionDetails(
        3, 'Ambiguous function reference due to multiple matches'
    )
    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_COLUMN = MisconceptionDetails(
        4, 'Reference to an undefined column in the database'
    )
    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_FUNCTION = MisconceptionDetails(
        5, 'Reference to an undefined function'
    )
    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_PARAMETER = MisconceptionDetails(
        6, 'Undefined parameter used in the query'
    )
    SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_OBJECT = MisconceptionDetails(
        7, 'General undefined object in query context'
    )
    SYN_2_UNDEFINED_DATABASE_OBJECT_INVALID_SCHEMA_NAME = MisconceptionDetails(
        8, 'Invalid schema name specified'
    )
    SYN_2_UNDEFINED_DATABASE_OBJECT_MISSPELLINGS = MisconceptionDetails(
        9, 'Misspellings in database object names'
    )
    SYN_2_UNDEFINED_DATABASE_OBJECT_SYNONYMS = MisconceptionDetails(
        10, 'Usage of synonyms instead of correct object names'
    )
    SYN_2_UNDEFINED_DATABASE_OBJECT_OMITTING_QUOTES_AROUND_CHARACTER_DATA = MisconceptionDetails(
        11, 'Omitting quotes around character data'
    )
    SYN_3_DATA_TYPE_MISMATCH_FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE = MisconceptionDetails(
        12, 'Failure to specify column name twice where required'
    )
    SYN_3_DATA_TYPE_MISMATCH = MisconceptionDetails(
        13, 'Mismatch between data types in query expressions'
    )
    SYN_4_ILLEGAL_AGGREGATE_FUNCTION_PLACEMENT_USING_AGGREGATE_FUNCTION_OUTSIDE_SELECT_OR_HAVING = MisconceptionDetails(
        14, 'Using aggregate functions outside SELECT or HAVING clauses'
    )
    SYN_4_ILLEGAL_AGGREGATE_FUNCTION_PLACEMENT_GROUPING_ERROR_AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED = MisconceptionDetails(
        15, 'Nesting aggregate functions where not allowed'
    )
    SYN_5_ILLEGAL_OR_INSUFFICIENT_GROUPING_GROUPING_ERROR_EXTRANEOUS_OR_OMITTED_GROUPING_COLUMN = MisconceptionDetails(
        16, 'Grouping error due to extraneous or omitted grouping column'
    )
    SYN_5_ILLEGAL_OR_INSUFFICIENT_GROUPING_STRANGE_HAVING_HAVING_WITHOUT_GROUP_BY = MisconceptionDetails(
        17, 'HAVING clause used without corresponding GROUP BY'
    )
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_FUNCTION_WITH_FUNCTION_PARAMETER = MisconceptionDetails(
        18, 'Confusing function name with function parameter'
    )
    SYN_6_COMMON_SYNTAX_ERROR_USING_WHERE_TWICE = MisconceptionDetails(
        19, 'Duplicate WHERE clause used'
    )
    SYN_6_COMMON_SYNTAX_ERROR_OMITTING_THE_FROM_CLAUSE = MisconceptionDetails(
        20, 'Omitting the FROM clause in a query'
    )
    SYN_6_COMMON_SYNTAX_ERROR_COMPARISON_WITH_NULL = MisconceptionDetails(
        21, 'Improper comparison with NULL'
    )
    SYN_6_COMMON_SYNTAX_ERROR_OMITTING_THE_SEMICOLON = MisconceptionDetails(
        22, 'Omitting semicolon at end of statement'
    )
    SYN_6_COMMON_SYNTAX_ERROR_DATE_TIME_FIELD_OVERFLOW = MisconceptionDetails(
        23, 'Date/time value overflow in query'
    )
    SYN_6_COMMON_SYNTAX_ERROR_DUPLICATE_CLAUSE = MisconceptionDetails(
        24, 'Duplicate clause within the same query'
    )
    SYN_6_COMMON_SYNTAX_ERROR_USING_AN_UNDEFINED_CORRELATION_NAME = MisconceptionDetails(
        25, 'Using an undefined correlation name'
    )
    SYN_6_COMMON_SYNTAX_ERROR_TOO_MANY_COLUMNS_IN_SUBQUERY = MisconceptionDetails(
        26, 'Excessive columns in a subquery result'
    )
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_TABLE_NAMES_WITH_COLUMN_NAMES = MisconceptionDetails(
        27, 'Confusing table names with column names'
    )
    SYN_6_COMMON_SYNTAX_ERROR_RESTRICTION_IN_SELECT_CLAUSE = MisconceptionDetails(
        28, 'Restriction added within the SELECT clause'
    )
    SYN_6_COMMON_SYNTAX_ERROR_PROJECTION_IN_WHERE_CLAUSE = MisconceptionDetails(
        29, 'Projection used in the WHERE clause'
    )
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_THE_ORDER_OF_KEYWORDS = MisconceptionDetails(
        30, 'Incorrect order of SQL keywords'
    )
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_THE_LOGIC_OF_KEYWORDS = MisconceptionDetails(
        31, 'Confusing logical functions of keywords'
    )
    SYN_6_COMMON_SYNTAX_ERROR_CONFUSING_THE_SYNTAX_OF_KEYWORDS = MisconceptionDetails(
        32, 'Syntax confusion in SQL keywords'
    )
    SYN_6_COMMON_SYNTAX_ERROR_OMITTING_COMMAS = MisconceptionDetails(
        33, 'Omitting commas between elements'
    )
    SYN_6_COMMON_SYNTAX_ERROR_CURLY_SQUARE_OR_UNMATCHED_BRACKETS = MisconceptionDetails(
        34, 'Unmatched or inappropriate brackets'
    )
    SYN_6_COMMON_SYNTAX_ERROR_IS_WHERE_NOT_APPLICABLE = MisconceptionDetails(
        35, 'Using IS in an incorrect context'
    )
    SYN_6_COMMON_SYNTAX_ERROR_NONSTANDARD_KEYWORDS_OR_STANDARD_KEYWORDS_IN_WRONG_CONTEXT = MisconceptionDetails(
        36, 'Nonstandard or misused keywords'
    )
    SYN_6_COMMON_SYNTAX_ERROR_NONSTANDARD_OPERATORS = MisconceptionDetails(
        37, 'Use of nonstandard operators'
    )
    SYN_6_COMMON_SYNTAX_ERROR_ADDITIONAL_SEMICOLON = MisconceptionDetails(
        38, 'Additional semicolon in query'
    )
    SEM_1_INCONSISTENT_EXPRESSION_AND_INSTEAD_OF_OR = MisconceptionDetails(
        39, 'Inconsistent expression: using AND instead of OR'
    )
    SEM_1_INCONSISTENT_EXPRESSION_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION = MisconceptionDetails(
        40, 'Inconsistent or tautological expression'
    )
    SEM_1_INCONSISTENT_EXPRESSION_DISTINCT_IN_SUM_OR_AVG = MisconceptionDetails(
        41, 'using DISTINCT used inside SUM or AVG to remove duplicate values outside of the aggregation'
    )
    SEM_1_INCONSISTENT_EXPRESSION_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES = MisconceptionDetails(
        42, 'DISTINCT usage potentially removing important duplicates'
    )
    SEM_1_INCONSISTENT_EXPRESSION_WILDCARDS_WITHOUT_LIKE = MisconceptionDetails(
        43, 'Wildcards used without LIKE'
    )
    SEM_1_INCONSISTENT_EXPRESSION_INCORRECT_WILDCARD_USING_UNDERSCORE_INSTEAD_OF_PERCENT = MisconceptionDetails(
        44, 'Incorrect wildcard: underscore instead of percent sign'
    )
    SEM_1_INCONSISTENT_EXPRESSION_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL = MisconceptionDetails(
        45, 'Mixing "> 0" with "IS NOT NULL"'
    )
    SEM_2_INCONSISTENT_JOIN_NULL_IN_SUBQUERY = MisconceptionDetails(
        46, 'NULL used improperly in subquery'
    )
    SEM_2_INCONSISTENT_JOIN_JOIN_ON_INCORRECT_COLUMN = MisconceptionDetails(
        47, 'Joining on an incorrect column'
    )
    SEM_3_MISSING_JOIN_OMITTING_A_JOIN = MisconceptionDetails(
        48, 'Omitted join leading to missing data'
    )
    SEM_4_DUPLICATE_ROWS_MANY_DUPLICATES = MisconceptionDetails(
        49, 'Duplicate rows where they are not necessary'
    )
    SEM_5_REDUNDANT_COLUMN_OUTPUT_CONSTANT_COLUMN_OUTPUT = MisconceptionDetails(
        50, 'Output includes redundant constant column'
    )
    SEM_5_REDUNDANT_COLUMN_OUTPUT_DUPLICATE_COLUMN_OUTPUT = MisconceptionDetails(
        51, 'Duplicate columns in output'
    )
    LOG_1_OPERATOR_ERROR_OR_INSTEAD_OF_AND = MisconceptionDetails(
        52, 'Using OR instead of AND, affecting result accuracy'
    )
    LOG_1_OPERATOR_ERROR_EXTRANEOUS_NOT_OPERATOR = MisconceptionDetails(
        53, 'Unnecessary NOT operator'
    )
    LOG_1_OPERATOR_ERROR_MISSING_NOT_OPERATOR = MisconceptionDetails(
        54, 'Missing NOT operator where required'
    )
    LOG_1_OPERATOR_ERROR_SUBSTITUTING_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO = MisconceptionDetails(
        55, 'Incorrect existence negation substitution'
    )
    LOG_1_OPERATOR_ERROR_PUTTING_NOT_IN_FRONT_OF_INCORRECT_IN_OR_EXISTS = MisconceptionDetails(
        56, 'Incorrect use of NOT with IN or EXISTS'
    )
    LOG_1_OPERATOR_ERROR_INCORRECT_COMPARISON_OPERATOR_OR_VALUE = MisconceptionDetails(
        57, 'Incorrect comparison operator or value'
    )
    LOG_2_JOIN_ERROR_JOIN_ON_INCORRECT_TABLE = MisconceptionDetails(
        58, 'Joining on incorrect table'
    )
    LOG_2_JOIN_ERROR_JOIN_WHEN_JOIN_NEEDS_TO_BE_OMITTED = MisconceptionDetails(
        59, 'Unnecessary join that should be omitted'
    )
    LOG_2_JOIN_ERROR_JOIN_ON_INCORRECT_COLUMN_MATCHES_POSSIBLE = MisconceptionDetails(
        60, 'Incorrect join column with possible matches'
    )
    LOG_2_JOIN_ERROR_JOIN_WITH_INCORRECT_COMPARISON_OPERATOR = MisconceptionDetails(
        61, 'Using incorrect comparison operator in join'
    )
    LOG_2_JOIN_ERROR_MISSING_JOIN = MisconceptionDetails(
        62, 'Missing join where required for result accuracy'
    )
    LOG_3_NESTING_ERROR_IMPROPER_NESTING_OF_EXPRESSIONS = MisconceptionDetails(
        63, 'Improper nesting of expressions in conditions'
    )
    LOG_3_NESTING_ERROR_IMPROPER_NESTING_OF_SUBQUERIES = MisconceptionDetails(
        64, 'Incorrect subquery nesting'
    )
    LOG_4_EXPRESSION_ERROR_EXTRANEOUS_QUOTES = MisconceptionDetails(
        65, 'Unnecessary quotes in expressions'
    )
    LOG_4_EXPRESSION_ERROR_MISSING_EXPRESSION = MisconceptionDetails(
        66, 'Expected expression missing in query'
    )
    LOG_4_EXPRESSION_ERROR_EXPRESSION_ON_INCORRECT_COLUMN = MisconceptionDetails(
        67, 'Expression used on an incorrect column'
    )
    LOG_4_EXPRESSION_ERROR_EXTRANEOUS_EXPRESSION = MisconceptionDetails(
        68, 'Superfluous expression included'
    )
    LOG_4_EXPRESSION_ERROR_EXPRESSION_IN_INCORRECT_CLAUSE = MisconceptionDetails(
        69, 'Expression used in incorrect clause'
    )
    LOG_5_PROJECTION_ERROR_EXTRANEOUS_COLUMN_IN_SELECT = MisconceptionDetails(
        70, 'Extraneous column included in SELECT clause'
    )
    LOG_5_PROJECTION_ERROR_MISSING_COLUMN_FROM_SELECT = MisconceptionDetails(
        71, 'Expected column missing from SELECT clause'
    )
    LOG_5_PROJECTION_ERROR_MISSING_DISTINCT_FROM_SELECT = MisconceptionDetails(
        72, 'Missing DISTINCT keyword in SELECT clause'
    )
    LOG_5_PROJECTION_ERROR_MISSING_AS_FROM_SELECT = MisconceptionDetails(
        73, 'Missing AS keyword for column alias in SELECT'
    )
    LOG_5_PROJECTION_ERROR_MISSING_COLUMN_FROM_ORDER_BY = MisconceptionDetails(
        74, 'Expected column missing from ORDER BY clause'
    )
    LOG_5_PROJECTION_ERROR_INCORRECT_COLUMN_IN_ORDER_BY = MisconceptionDetails(
        75, 'Incorrect column used in ORDER BY clause'
    )
    LOG_5_PROJECTION_ERROR_EXTRANEOUS_ORDER_BY_CLAUSE = MisconceptionDetails(
        76, 'Unnecessary ORDER BY clause used'
    )
    LOG_5_PROJECTION_ERROR_INCORRECT_ORDERING_OF_ROWS = MisconceptionDetails(
        77, 'Incorrect row ordering in query result'
    )
    LOG_6_FUNCTION_ERROR_DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE = MisconceptionDetails(
        78, 'DISTINCT used as a function parameter unnecessarily'
    )
    LOG_6_FUNCTION_ERROR_MISSING_DISTINCT_FROM_FUNCTION_PARAMETER = MisconceptionDetails(
        79, 'DISTINCT omitted as function parameter when required'
    )
    LOG_6_FUNCTION_ERROR_INCORRECT_FUNCTION = MisconceptionDetails(
        80, 'Incorrect function used for the given data demand'
    )
    LOG_6_FUNCTION_ERROR_INCORRECT_COLUMN_AS_FUNCTION_PARAMETER = MisconceptionDetails(
        81, 'Incorrect column used as function parameter'
    )
    COM_1_COMPLICATION_UNNECESSARY_COMPLICATION = MisconceptionDetails(
        82, 'Query is unnecessarily complicated'
    )
    COM_1_COMPLICATION_UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE = MisconceptionDetails(
        83, 'Unnecessary DISTINCT keyword in SELECT clause'
    )
    COM_1_COMPLICATION_UNNECESSARY_JOIN = MisconceptionDetails(
        84, 'Unnecessary join operation'
    )
    COM_1_COMPLICATION_UNUSED_CORRELATION_NAME = MisconceptionDetails(
        85, 'Correlation name defined but never used'
    )
    COM_1_COMPLICATION_CORRELATION_NAMES_ARE_ALWAYS_IDENTICAL = MisconceptionDetails(
        86, 'Identical correlation names used unnecessarily'
    )
    COM_1_COMPLICATION_UNNECESSARILY_GENERAL_COMPARISON_OPERATOR = MisconceptionDetails(
        87, 'Overly general comparison operator used'
    )
    COM_1_COMPLICATION_LIKE_WITHOUT_WILDCARDS = MisconceptionDetails(
        88, 'LIKE operator used without wildcards'
    )
    COM_1_COMPLICATION_UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY = MisconceptionDetails(
        89, 'SELECT clause in EXISTS subquery is overly complicated'
    )
    COM_1_COMPLICATION_IN_EXISTS_CAN_BE_REPLACED_BY_COMPARISON = MisconceptionDetails(
        90, 'IN/EXISTS subquery could be replaced by a simple comparison'
    )
    COM_1_COMPLICATION_UNNECESSARY_AGGREGATE_FUNCTION = MisconceptionDetails(
        91, 'Unnecessary aggregate function used in query'
    )
    COM_1_COMPLICATION_UNNECESSARY_DISTINCT_IN_AGGREGATE_FUNCTION = MisconceptionDetails(
        92, 'DISTINCT unnecessarily used in aggregate function'
    )
    COM_1_COMPLICATION_UNNECESSARY_ARGUMENT_OF_COUNT = MisconceptionDetails(
        93, 'COUNT function includes unnecessary argument'
    )
    COM_1_COMPLICATION_UNNECESSARY_GROUP_BY_IN_EXISTS_SUBQUERY = MisconceptionDetails(
        94, 'GROUP BY clause used unnecessarily in EXISTS subquery'
    )
    COM_1_COMPLICATION_GROUP_BY_WITH_SINGLETON_GROUPS = MisconceptionDetails(
        95, 'GROUP BY clause creates singleton groups unnecessarily'
    )
    COM_1_COMPLICATION_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT = MisconceptionDetails(
        96, 'GROUP BY clause could be replaced by DISTINCT'
    )
    COM_1_COMPLICATION_UNION_CAN_BE_REPLACED_BY_OR = MisconceptionDetails(
        97, 'UNION operation could be replaced by OR condition'
    )
    COM_1_COMPLICATION_UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE = MisconceptionDetails(
        99, 'Unnecessary column specified in ORDER BY clause'
    )
    COM_1_COMPLICATION_ORDER_BY_IN_SUBQUERY = MisconceptionDetails(
        100, 'ORDER BY clause used in subquery unnecessarily'
    )
    COM_1_COMPLICATION_INEFFICIENT_HAVING = MisconceptionDetails(
        101, 'Inefficient HAVING clause'
    )
    COM_1_COMPLICATION_INEFFICIENT_UNION = MisconceptionDetails(
        102, 'Inefficient use of UNION operation'
    )
    COM_1_COMPLICATION_CONDITION_IN_SUBQUERY_CAN_BE_MOVED_UP = MisconceptionDetails(
        103, 'Condition in subquery could be moved up for efficiency'
    )
    COM_1_COMPLICATION_CONDITION_ON_LEFT_TABLE_IN_LEFT_OUTER_JOIN = MisconceptionDetails(
        104, 'Condition applied to left table in LEFT OUTER JOIN unnecessarily'
    )
    COM_1_COMPLICATION_OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN = MisconceptionDetails(
        105, 'Outer join used when inner join would suffice'
    )
    COM_X_COMPLICATION_JOIN_CONDITION_IN_WHERE_CLAUSE = MisconceptionDetails(
        106, 'Join condition specified in WHERE clause instead of ON clause'
    )
