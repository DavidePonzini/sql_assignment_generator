# In error_details.py
from typing import List, Dict
from dataclasses import dataclass
from .difficulty_level import DifficultyLevel
from sql_error_categorizer.sql_errors import SqlErrors

#inner query gli fa schifo a chatgpt
@dataclass
class SqlErrorDetails:
    description: str
    characteristics: str
    constraints: Dict[DifficultyLevel, List[str]]
    
ERROR_DETAILS_MAP ={
    SqlErrors.SYN_2_AMBIGUOUS_COLUMN: SqlErrorDetails(
        description="Ambiguous column",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers SQL error code 42702, to cause this, " \
            "it is necessary to make some column names from different tables the same.",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS x table", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table ", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_4_UNDEFINED_COLUMN: SqlErrorDetails(  #similar to 9
        description="Undefined column",
        characteristics = "exercise should naturally tempts student to make a mistake that triggers SQL error code 42703; to cause this, " \
            "it is necessary to make the column name more complex or longer.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 1 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 WHERE condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_7_UNDEFINED_OBJECT: SqlErrorDetails(  #similar to 9
        description="Undefined object",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers SQL error code 42704, " \
            "to cause this, it is necessary to make the table name more complex or longer.",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS x table"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have2-6 COLUMNS x table", "must have 2 WHERE condition", "must have SUB-QUERY","must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_8_INVALID_SCHEMA_NAME: SqlErrorDetails(
        description="Invalid schema name",
        characteristics = "It is necessary include the schema name when creating the table in order to produce a student mistake that " \
            "triggers SQL error code 3F000. Create different table of different schema (more than 2 schema)",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS x table", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 3 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SYN_9_MISSPELLINGS: SqlErrorDetails(  #similar to 4 and 7
        description="Misspellings",
        characteristics ="a query that can cause errors possibly due to typos — for example, " \
            "by generating tables and COLUMNS with complex names (students may mistype them) or with very similar names (e.g., name and names).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 1 COLUMNS x table", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 WHERE condition", "must have 2 similar column"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 4 similar column", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_10_SYNONYMS: SqlErrorDetails(
        description="Synonyms",
        characteristics ="exercise should naturally tempts student to make a mistake because students may misremember the correct name — for example, " \
            "by creating tables and COLUMNS with similar names (like competition and competitor) or similar meanings (like monster and zombie).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 similar column"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 3-5 COLUMNS x table", "must have 3 similar column", "must have 2 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 2 table with similar meaning", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_11_OMITTING_QUOTES_AROUND_CHARACTER_DATA: SqlErrorDetails(
        description="Omitting quotes around character data",
        characteristics ="exercise should naturally tempts student to make a mistake of the type “strings not quoted,” " \
            "requiring string operations in the WHERE clause involving many string variables.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 1 WHERE string condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 WHERE string condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 WHERE string condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_12_FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE: SqlErrorDetails(
        description="Failure to specify column name twice",
        characteristics ="exercise should naturally tempts student to make a mistake that can cause “strings not quoted” errors; " \
            "therefore, the query should include multiple conditions on the same column.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 1 multiple WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have2-4 COLUMNS x table", "must have 2 multiple WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 multiple WHERE condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_15_AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED: SqlErrorDetails(
        description="Grouping error: aggregate functions cannot be nested",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers SQL error code 42803 " \
            "by generating a query in natural language that seems to involve one AGGREGATION inside another " \
            "(e.g. “the book that has the maximum number of sales,” and in database doesn't store the sales count).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 1 AGGREGATION"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have SUB-QUERY", "must have 2 AGGREGATION"]
        }
    ),
    SqlErrors.SYN_19_USING_WHERE_TWICE: SqlErrorDetails(
        description="Using WHERE twice",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers use of multiple WHERE",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 WHERE condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_21_COMPARISON_WITH_NULL: SqlErrorDetails(
        description="Comparison with NULL",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers use of equal (=) in presence of NULL, some column must be nullable",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 WHERE condition", "must have SUB-QUERY", "must have 2 AGGREGATION"]
        }
    ),
    SqlErrors.SYN_26_TOO_MANY_COLUMNS_IN_SUBQUERY: SqlErrorDetails(
        description="Too many COLUMNS in subquery",
        characteristics ="exercise should naturally tempts student to make a mistake which consists in inserting many column in subquery." \
            " The query in solution is mandatory that have subquery to trigger error in student",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 WHERE condition", "must have 2 AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SYN_35_IS_WHERE_NOT_APPLICABLE: SqlErrorDetails(
        description="Use 'IS' where it's not applicable",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in use IS with condition not null (e.g. female IS true)." \
        "The query in solution is mandatory that have many WHERE condition with different type (boolean, integer, string, NULL)",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-4 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_39_AND_INSTEAD_OF_OR: SqlErrorDetails(
        description="AND instead of OR",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in use AND respect to OR. " \
            "The query in solution is mandatory that have many WHERE condition which using AND with two conditions that are mutually exclusive, " \
            "resulting always in an empty result set (ex. p.city='Genova' AND p.city='Rome' )",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_40_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION: SqlErrorDetails(##########################################
        description="Implied, tautological or inconsistent expression",
        characteristics ="",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", ""],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "", ""],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", ""]
        }
    ),
    SqlErrors.SEM_41_DISTINCT_IN_SUM_OR_AVG: SqlErrorDetails(
        description="Use DISTINCT into SUM or AVG",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in use DISTINCT inside AVG or SUM. " \
            "The query in solution is mandatory that have many AGGREGATION of type AVG or SUM",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have AVG or SUM AGGREGATION", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 AVG or SUM AGGREGATION", "must have 2 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 AVG or SUM AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    # SEM_41_DISTINCT_IN_SUM_OR_AVG                                       
    # SEM_42_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES              
    # SEM_43_WILDCARDS_WITHOUT_LIKE                                        
    # SEM_44_INCORRECT_WILDCARD                                           
    # SEM_45_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL                     
    # SEM_46_NULL_IN_IN_ANY_ALL_SUBQUERY 
    # SEM_49_MANY_DUPLICATES                                              
    # SEM_50_CONSTANT_COLUMN_OUTPUT 
    # LOG_52_OR_INSTEAD_OF_AND                                            
    # LOG_53_EXTRANEOUS_NOT_OPERATOR                                      
    # LOG_54_MISSING_NOT_OPERATOR                                         
    # LOG_55_SUBSTITUTING_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO            
    # LOG_56_PUTTING_NOT_IN_FRONT_OF_INCORRECT_IN_OR_EXISTS               
    # LOG_57_INCORRECT_COMPARISON_OPERATOR_OR_VALUE                       
    # LOG_58_JOIN_ON_INCORRECT_TABLE                                      
    # LOG_59_JOIN_WHEN_JOIN_NEEDS_TO_BE_OMITTED                           
    # LOG_60_JOIN_ON_INCORRECT_COLUMN_MATCHES_POSSIBLE 
    # LOG_62_MISSING_JOIN                                                 
    # LOG_63_MPROPER_NESTING_OF_EXPRESSIONS                               
    # LOG_64_IMPROPER_NESTING_OF_SUBQUERIES 
    # LOG_66_MISSING_EXPRESSION                                           
    # LOG_67_EXPRESSION_ON_INCORRECT_COLUMN                               
    # LOG_68_EXTRANEOUS_EXPRESSION                                        
    # LOG_69_EXPRESSION_IN_INCORRECT_CLAUSE                               
    # LOG_70_EXTRANEOUS_COLUMN_IN_SELECT                                  
    # LOG_71_MISSING_COLUMN_FROM_SELECT                                   
    # LOG_72_MISSING_DISTINCT_FROM_SELECT                                 
    # LOG_73_MISSING_AS_FROM_SELECT                                       
    # LOG_74_MISSING_COLUMN_FROM_ORDER_BY                                 
    # LOG_75_INCORRECT_COLUMN_IN_ORDER_BY                                 
    # LOG_76_EXTRANEOUS_ORDER_BY_CLAUSE                                   
    # LOG_77_INCORRECT_ORDERING_OF_ROWS                                   
    # LOG_78_DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE          
    # LOG_79_MISSING_DISTINCT_FROM_FUNCTION_PARAMETER                     
    # LOG_80_INCORRECT_FUNCTION                                           
    # LOG_81_INCORRECT_COLUMN_AS_FUNCTION_PARAMETER
    # COM_83_UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE                        
    # COM_84_UNNECESSARY_JOIN 
    # COM_86_CORRELATION_NAMES_ARE_ALWAYS_IDENTICAL
    # COM_88_LIKE_WITHOUT_WILDCARDS                                       
    # COM_89_UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY 
    # COM_91_UNNECESSARY_AGGREGATE_FUNCTION
    # COM_93_UNNECESSARY_ARGUMENT_OF_COUNT
    # COM_95_GROUP_BY_WITH_SINGLETON_GROUPS                               
    # COM_96_GROUP_BY_WITH_ONLY_A_SINGLE_GROUP                            
    # COM_97_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT                       
    # COM_98_UNION_CAN_BE_REPLACED_BY_OR                                  
    # COM_99_UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE
    # COM_102_INEFFICIENT_UNION
    # COM_104_CONDITION_ON_LEFT_TABLE_IN_LEFT_OUTER_JOIN                 
    # COM_105_OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN
}