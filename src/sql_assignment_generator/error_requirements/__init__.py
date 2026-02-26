from sql_error_taxonomy import SqlErrors

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
from .err_058 import Err058_JoinOnIncorrectTable
from .err_059 import Err059_JoinWhenJoinNeedsToBeOmitted
from .err_060 import Err060_JoinOnIncorrectColumn
from .err_062 import Err062_MissingJoin
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
from .err_084 import Err084_UnncessaryJoin
from .err_086 import Err086_CorrelationNamesAreAlwaysIdentical
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
from .err_104 import Err104_ConditionOnLeftTableInLeftOuterJoin
from .err_105 import Err105_OuterJoinCanBeReplacedByInnerJoin


ERROR_REQUIREMENTS_MAP: dict[SqlErrors, type[SqlErrorRequirements]] = {
    SqlErrors.SYN_2_AMBIGUOUS_COLUMN:                                           Err002_AmbiguousColumn,
    SqlErrors.SYN_4_UNDEFINED_COLUMN:                                           Err004_UndefinedColumn,
    SqlErrors.SYN_7_UNDEFINED_OBJECT:                                           Err007_UndefinedObject,
    SqlErrors.SYN_9_MISSPELLINGS:                                               Err009_Misspellings,
    SqlErrors.SYN_10_SYNONYMS:                                                  Err010_Synonyms,
    SqlErrors.SYN_11_OMITTING_QUOTES_AROUND_CHARACTER_DATA:                     Err011_OmittingQuotesAroundCharacterData,
    SqlErrors.SYN_12_FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE:                      Err012_FailureToSpecifyColumnNameTwice,
    SqlErrors.SYN_15_AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED:                      Err015_AggregateFunctionsCannotBeNested,
    SqlErrors.SYN_19_USING_WHERE_TWICE:                                         Err019_UsingWhereTwice,
    SqlErrors.SYN_21_COMPARISON_WITH_NULL:                                      Err021_ComparisonWithNull,
    SqlErrors.SYN_26_TOO_MANY_COLUMNS_IN_SUBQUERY:                              Err026_TooManyColumnsInSubquery,
    SqlErrors.SYN_35_IS_WHERE_NOT_APPLICABLE:                                   Err035_IsWhereNotApplicable,
    SqlErrors.SEM_39_AND_INSTEAD_OF_OR:                                         Err039_AndInsteadOfOr,
    SqlErrors.SEM_40_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION:                   Err040_ImpliedTautologicalOrInconsistentExpressions,
    SqlErrors.SEM_41_DISTINCT_IN_SUM_OR_AVG:                                    Err041_DistinctInSumOrAvg,
    SqlErrors.SEM_42_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES:           Err042_DistinctThatMightRemoveImportantDuplicates,
    SqlErrors.SEM_43_WILDCARDS_WITHOUT_LIKE:                                    Err043_WildcardsWithoutLike,
    SqlErrors.SEM_44_INCORRECT_WILDCARD:                                        Err044_IncorrectWildcard,
    SqlErrors.SEM_45_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL:                  Err045_MixingGT0WithIsNotNullOrEmptyStringWithNull,
    SqlErrors.SEM_46_NULL_IN_IN_ANY_ALL_SUBQUERY:                               Err046_NullInInAnyAllSubquery,
    SqlErrors.SEM_49_MANY_DUPLICATES:                                           Err049_ManyDuplicates,
    SqlErrors.LOG_52_OR_INSTEAD_OF_AND:                                         Err052_OrInsteadOfAnd,
    SqlErrors.LOG_53_EXTRANEOUS_NOT_OPERATOR:                                   Err053_ExtraneousNot,
    SqlErrors.LOG_54_MISSING_NOT_OPERATOR:                                      Err054_MissingNot,
    SqlErrors.LOG_55_SUBSTITUTING_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO:         Err055_SubstitutingExistanceNegation,
    SqlErrors.LOG_57_INCORRECT_COMPARISON_OPERATOR_OR_VALUE:                    Err057_IncorrectComparisonOperatorOrIncorrectValueCompared,
    SqlErrors.LOG_58_JOIN_ON_INCORRECT_TABLE:                                   Err058_JoinOnIncorrectTable,
    SqlErrors.LOG_59_JOIN_WHEN_JOIN_NEEDS_TO_BE_OMITTED:                        Err059_JoinWhenJoinNeedsToBeOmitted,
    SqlErrors.LOG_60_JOIN_ON_INCORRECT_COLUMN_MATCHES_POSSIBLE:                 Err060_JoinOnIncorrectColumn,
    SqlErrors.LOG_62_MISSING_JOIN:                                              Err062_MissingJoin,
    SqlErrors.LOG_63_IMPROPER_NESTING_OF_EXPRESSIONS:                           Err063_ImproperNestingOfExpressions,
    SqlErrors.LOG_64_IMPROPER_NESTING_OF_SUBQUERIES:                            Err064_ImproperNestingOfSubqueries,
    SqlErrors.LOG_66_MISSING_EXPRESSION:                                        Err066_MissingExpression,
    SqlErrors.LOG_67_EXPRESSION_ON_INCORRECT_COLUMN:                            Err067_ExpressionOnIncorrectColumn,
    SqlErrors.LOG_68_EXTRANEOUS_EXPRESSION:                                     Err068_ExtraneousExpression,
    SqlErrors.LOG_69_EXPRESSION_IN_INCORRECT_CLAUSE:                            Err069_ExpressionInIncorrectClause,
    SqlErrors.LOG_70_EXTRANEOUS_COLUMN_IN_SELECT:                               Err070_ExtraneousColumnInSelect,
    SqlErrors.LOG_71_MISSING_COLUMN_FROM_SELECT:                                Err071_MissingColumnFromSelect,
    SqlErrors.LOG_72_MISSING_DISTINCT_FROM_SELECT:                              Err072_MissingDistinctFromSelect,
    SqlErrors.LOG_73_MISSING_AS_FROM_SELECT:                                    Err073_MissingAsFromSelect,
    SqlErrors.LOG_74_MISSING_COLUMN_FROM_ORDER_BY:                              Err074_MissingColumnFromOrderByClause,
    SqlErrors.LOG_75_INCORRECT_COLUMN_IN_ORDER_BY:                              Err075_IncorrectColumnInOrderByClause,
    SqlErrors.LOG_76_EXTRANEOUS_ORDER_BY_CLAUSE:                                Err076_ExtraneousOrderByClause,
    SqlErrors.LOG_77_INCORRECT_ORDERING_OF_ROWS:                                Err077_IncorrectOrderingOfRows,
    SqlErrors.LOG_78_DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE:       Err078_DistinctAsFunctionParameterWhereNotApplicable,
    SqlErrors.LOG_79_MISSING_DISTINCT_FROM_FUNCTION_PARAMETER:                  Err079_MissingDistinctFromFunctionParameter,
    SqlErrors.LOG_80_INCORRECT_FUNCTION:                                        Err080_IncorrectFunction,
    SqlErrors.LOG_81_INCORRECT_COLUMN_AS_FUNCTION_PARAMETER:                    Err081_IncorrectColumnAsFunctionParamether,
    SqlErrors.COM_83_UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE:                     Err083_UnnecessaryDistinctInSelectClause,
    SqlErrors.COM_84_UNNECESSARY_JOIN:                                          Err084_UnncessaryJoin,
    SqlErrors.COM_86_CORRELATION_NAMES_ARE_ALWAYS_IDENTICAL:                    Err086_CorrelationNamesAreAlwaysIdentical,
    SqlErrors.COM_88_LIKE_WITHOUT_WILDCARDS:                                    Err088_LikeWithoutWildcards,
    SqlErrors.COM_89_UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY:       Err089_UnnecessarilyComplicatedSelectInExistsSubquery,
    SqlErrors.COM_91_UNNECESSARY_AGGREGATE_FUNCTION:                            Err091_UnnessaryAggregateFunction,
    SqlErrors.COM_93_UNNECESSARY_ARGUMENT_OF_COUNT:                             Err093_UnnecessaryArgumentOfCount,
    SqlErrors.COM_95_GROUP_BY_WITH_SINGLETON_GROUPS:                            Err095_GroupByWithSingletonGroups,
    SqlErrors.COM_96_GROUP_BY_WITH_ONLY_A_SINGLE_GROUP:                         Err096_GroupByWithOnlyASingleGroup,
    SqlErrors.COM_97_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT:                    Err097_GroupByCanBeReplacedWithDistinct,
    SqlErrors.COM_98_UNION_CAN_BE_REPLACED_BY_OR:                               Err098_UnionByCanReplacedByOr,
    SqlErrors.COM_99_UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE:                     Err099_UnnecessaryColumnInOrderByClause,
    SqlErrors.COM_102_INEFFICIENT_UNION:                                        Err102_InefficientUnion,
    SqlErrors.COM_104_CONDITION_ON_LEFT_TABLE_IN_LEFT_OUTER_JOIN:               Err104_ConditionOnLeftTableInLeftOuterJoin,
    SqlErrors.COM_105_OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN:                 Err105_OuterJoinCanBeReplacedByInnerJoin,
}
'''Mapping of SQL errors to their requirements.'''
