from sqlerrors import SqlErrors

from .base import SqlErrorRequirements

# requirement for all supported errors
from .err_002 import Err002_AmbiguousColumn
from .err_004 import Err004_UndefinedColumn
from .err_007 import Err007_UndefinedObject
from .err_009 import Err009_Misspellings
from .err_010 import Err010_Synonyms
from .err_011 import Err011_OmittingQuotesAroundCharacterData
from .err_012 import Err012_FailureToSpecifyColumnNameTwice
from .err_015 import Err015_AggregateFunctionsCannotBeNested
from .err_019 import Err019_UsingWhereTwice
from .err_021 import Err021_ComparisonWithNull
from .err_026 import Err026_TooManyColumnsInSubquery
from .err_035 import Err035_IsWhereNotApplicable
from .err_039 import Err039_AndInsteadOfOr
from .err_040 import Err040_ImpliedTautologicalOrInconsistentExpressions
from .err_041 import Err041_DistinctInSumOrAvg
from .err_042 import Err042_DistinctThatMightRemoveImportantDuplicates
from .err_043 import Err043_WildcardsWithoutLike
from .err_044 import Err044_IncorrectWildcard
from .err_045 import Err045_MixingGT0WithIsNotNullOrEmptyStringWithNull
from .err_046 import Err046_NullInInAnyAllSubquery
from .err_049 import Err049_ManyDuplicates
from .err_052 import Err052_OrInsteadOfAnd
from .err_053 import Err053_ExtraneousNot
from .err_054 import Err054_MissingNot
from .err_055 import Err055_SubstitutingExistanceNegation
from .err_057 import Err057_IncorrectComparisonOperatorOrIncorrectValueCompared
from .err_058 import Err058_IncorrectTableReference
from .err_059 import Err059_ExtraneousTableReference
from .err_060 import Err060_JoinConditionOnIncorrectColumn
from .err_062 import Err062_MissingTableReference
from .err_063 import Err063_ImproperNestingOfExpressions
from .err_064 import Err064_ImproperNestingOfSubqueries
from .err_066 import Err066_MissingExpression
from .err_067 import Err067_ExpressionOnIncorrectColumn
from .err_068 import Err068_ExtraneousExpression
from .err_069 import Err069_ExpressionInIncorrectClause
from .err_070 import Err070_ExtraneousColumnInSelect
from .err_071 import Err071_MissingColumnFromSelect
from .err_072 import Err072_MissingDistinctFromSelect
from .err_073 import Err073_MissingAsFromSelect
from .err_074 import Err074_MissingColumnFromOrderByClause
from .err_075 import Err075_IncorrectColumnInOrderByClause
from .err_076 import Err076_ExtraneousOrderByClause
from .err_077 import Err077_IncorrectOrderingOfRows
from .err_078 import Err078_DistinctAsFunctionParameterWhereNotApplicable
from .err_079 import Err079_MissingDistinctFromFunctionParameter
from .err_080 import Err080_IncorrectFunction
from .err_081 import Err081_IncorrectColumnAsFunctionParamether
from .err_083 import Err083_UnnecessaryDistinctInSelectClause
from .err_084 import Err084_UnncessaryTableReference
from .err_086 import Err086_TablesHaveTheSameData
from .err_088 import Err088_LikeWithoutWildcards
from .err_089 import Err089_UnnecessarilyComplicatedSelectInExistsSubquery
from .err_091 import Err091_UnnessaryAggregateFunction
from .err_093 import Err093_UnnecessaryArgumentOfCount
from .err_095 import Err095_GroupByWithSingletonGroups
from .err_096 import Err096_GroupByWithOnlyASingleGroup
from .err_097 import Err097_GroupByCanBeReplacedWithDistinct
from .err_098 import Err098_UnionByCanReplacedByOr
from .err_099 import Err099_UnnecessaryColumnInOrderByClause
from .err_102 import Err102_InefficientUnion
from .err_104 import Err104_ConditionOnOuterJoin
from .err_105 import Err105_OuterJoinCanBeReplacedByInnerJoin
from .err_110 import Err110_WrongWildcard
from .err_111 import Err111_InvalidWildcard


ERROR_REQUIREMENTS_MAP: dict[SqlErrors, type[SqlErrorRequirements]] = {
    SqlErrors.AMBIGUOUS_COLUMN:                                                     Err002_AmbiguousColumn,
    SqlErrors.UNDEFINED_COLUMN:                                                     Err004_UndefinedColumn,
    SqlErrors.UNDEFINED_OBJECT:                                                     Err007_UndefinedObject,
    SqlErrors.MISSPELLINGS:                                                         Err009_Misspellings,
    SqlErrors.SYNONYMS:                                                             Err010_Synonyms,
    SqlErrors.OMITTED_QUOTES:                                                       Err011_OmittingQuotesAroundCharacterData,
    SqlErrors.FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE:                                 Err012_FailureToSpecifyColumnNameTwice,
    SqlErrors.AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED:                                 Err015_AggregateFunctionsCannotBeNested,
    SqlErrors.USING_WHERE_TWICE:                                                    Err019_UsingWhereTwice,
    SqlErrors.COMPARISON_WITH_NULL:                                                 Err021_ComparisonWithNull,
    SqlErrors.TOO_MANY_COLUMNS_IN_SUBQUERY:                                         Err026_TooManyColumnsInSubquery,
    SqlErrors.IS_WHERE_NOT_APPLICABLE:                                              Err035_IsWhereNotApplicable,
    SqlErrors.AND_INSTEAD_OF_OR:                                                    Err039_AndInsteadOfOr,
    SqlErrors.IMPLIED_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION:                      Err040_ImpliedTautologicalOrInconsistentExpressions,
    SqlErrors.DISTINCT_IN_SUM_OR_AVG:                                               Err041_DistinctInSumOrAvg,
    SqlErrors.DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES:                      Err042_DistinctThatMightRemoveImportantDuplicates,
    SqlErrors.WILDCARDS_WITHOUT_LIKE:                                               Err043_WildcardsWithoutLike,
    SqlErrors.INCORRECT_WILDCARD:                                                   Err044_IncorrectWildcard,
    SqlErrors.WRONG_WILDCARD:                                                       Err110_WrongWildcard,
    SqlErrors.INVALID_WILDCARD:                                                     Err111_InvalidWildcard,
    SqlErrors.MIXED_A_GREATER_THAN_0_WITH_IS_NOT_NULL_OR_EMPTY_STRING_WITH_NULL:    Err045_MixingGT0WithIsNotNullOrEmptyStringWithNull,
    SqlErrors.NULL_IN_IN_ANY_ALL_SUBQUERY:                                          Err046_NullInInAnyAllSubquery,
    SqlErrors.MANY_DUPLICATES:                                                      Err049_ManyDuplicates,
    SqlErrors.OR_INSTEAD_OF_AND:                                                    Err052_OrInsteadOfAnd,
    SqlErrors.EXTRANEOUS_NOT_OPERATOR:                                              Err053_ExtraneousNot,
    SqlErrors.MISSING_NOT_OPERATOR:                                                 Err054_MissingNot,
    SqlErrors.SUBSTITUTED_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO:                     Err055_SubstitutingExistanceNegation,
    SqlErrors.INCORRECT_COMPARISON_OPERATOR_OR_INCORRECT_VALUE_COMPARED:            Err057_IncorrectComparisonOperatorOrIncorrectValueCompared,
    SqlErrors.INCORRECT_TABLE_REFERENCE:                                            Err058_IncorrectTableReference,
    SqlErrors.EXTRANEOUS_TABLE_REFERENCE:                                           Err059_ExtraneousTableReference,
    SqlErrors.JOIN_CONDITION_ON_INCORRECT_COLUMN:                                   Err060_JoinConditionOnIncorrectColumn,
    SqlErrors.MISSING_TABLE_REFERENCE:                                              Err062_MissingTableReference,
    SqlErrors.IMPROPER_NESTING_OF_EXPRESSIONS:                                      Err063_ImproperNestingOfExpressions,
    SqlErrors.IMPROPER_NESTING_OF_SUBQUERIES:                                       Err064_ImproperNestingOfSubqueries,
    SqlErrors.MISSING_EXPRESSION:                                                   Err066_MissingExpression,
    SqlErrors.EXPRESSION_ON_INCORRECT_COLUMN:                                       Err067_ExpressionOnIncorrectColumn,
    SqlErrors.EXTRANEOUS_EXPRESSION:                                                Err068_ExtraneousExpression,
    SqlErrors.EXPRESSION_IN_INCORRECT_CLAUSE:                                       Err069_ExpressionInIncorrectClause,
    SqlErrors.EXTRANEOUS_COLUMN_IN_SELECT:                                          Err070_ExtraneousColumnInSelect,
    SqlErrors.MISSING_COLUMN_FROM_SELECT:                                           Err071_MissingColumnFromSelect,
    SqlErrors.MISSING_DISTINCT_FROM_SELECT:                                         Err072_MissingDistinctFromSelect,
    SqlErrors.MISSING_AS_FROM_SELECT:                                               Err073_MissingAsFromSelect,
    SqlErrors.MISSING_COLUMN_FROM_ORDER_BY_CLAUSE:                                  Err074_MissingColumnFromOrderByClause,
    SqlErrors.INCORRECT_COLUMN_IN_ORDER_BY_CLAUSE:                                  Err075_IncorrectColumnInOrderByClause,
    SqlErrors.EXTRANEOUS_ORDER_BY_CLAUSE:                                           Err076_ExtraneousOrderByClause,
    SqlErrors.INCORRECT_ORDERING_OF_ROWS:                                           Err077_IncorrectOrderingOfRows,
    SqlErrors.DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE:                  Err078_DistinctAsFunctionParameterWhereNotApplicable,
    SqlErrors.MISSING_DISTINCT_FROM_FUNCTION_PARAMETER:                             Err079_MissingDistinctFromFunctionParameter,
    SqlErrors.INCORRECT_FUNCTION:                                                   Err080_IncorrectFunction,
    SqlErrors.INCORRECT_COLUMN_AS_FUNCTION_PARAMETER:                               Err081_IncorrectColumnAsFunctionParamether,
    SqlErrors.UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE:                                Err083_UnnecessaryDistinctInSelectClause,
    SqlErrors.UNNECESSARY_TABLE_REFERENCE:                                          Err084_UnncessaryTableReference,
    SqlErrors.TABLES_HAVE_SAME_DATA:                                                Err086_TablesHaveTheSameData,
    SqlErrors.LIKE_WITHOUT_WILDCARDS:                                               Err088_LikeWithoutWildcards,
    SqlErrors.UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY:                  Err089_UnnecessarilyComplicatedSelectInExistsSubquery,
    SqlErrors.UNNECESSARY_AGGREGATE_FUNCTION:                                       Err091_UnnessaryAggregateFunction,
    SqlErrors.UNNECESSARY_ARGUMENT_OF_COUNT:                                        Err093_UnnecessaryArgumentOfCount,
    SqlErrors.GROUP_BY_WITH_SINGLETON_GROUPS:                                       Err095_GroupByWithSingletonGroups,
    SqlErrors.GROUP_BY_WITH_ONLY_A_SINGLE_GROUP:                                    Err096_GroupByWithOnlyASingleGroup,
    SqlErrors.GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT:                               Err097_GroupByCanBeReplacedWithDistinct,
    SqlErrors.UNION_CAN_BE_REPLACED_BY_OR:                                          Err098_UnionByCanReplacedByOr,
    SqlErrors.UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE:                                Err099_UnnecessaryColumnInOrderByClause,
    SqlErrors.INEFFICIENT_UNION:                                                    Err102_InefficientUnion,
    SqlErrors.CONDITION_ON_OUTER_JOIN:                                              Err104_ConditionOnOuterJoin,
    SqlErrors.OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN:                             Err105_OuterJoinCanBeReplacedByInnerJoin,
}
'''Mapping of SQL errors to their requirements.'''
