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
        characteristics ="exercise should naturally tempts student to make a mistake that triggers SQL error code 42702. " \
            "In table creation must make some column names from different tables the same.",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS x table", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table ", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_4_UNDEFINED_COLUMN: SqlErrorDetails(
        description="Undefined column",
        characteristics = "exercise should naturally tempts student to make a mistake that triggers SQL error code 42703; to cause this, " \
            "it is necessary to make the column name more complex or longer.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 1 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 WHERE condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_7_UNDEFINED_OBJECT: SqlErrorDetails(
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
    SqlErrors.SYN_9_MISSPELLINGS: SqlErrorDetails(
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
            "It is mandatory use WHERE clause involving in many condition with STRING variables (e.g. name = 'value').",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 1 WHERE STRING condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 WHERE STRING condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 WHERE STRING condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_12_FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE: SqlErrorDetails( #non funziona sempre se metto da 3 in poi multiple cond.
        description="Failure to specify column name twice",
        characteristics = "Solution query must have MULTIPLE CONDITION on the SAME COLUMN (e.g. p.film='Alien' OR/AND p.film='Superman' this represent one column with MULTIPLE CONDITION). " \
            "Solution must not have IN format like 'position IN ('Manager', 'Supervisor')' but I want  this format 'position ='Manager' OR position = 'Supervisor''" \
            "exercise should naturally tempts student to make a mistake that can cause “miss column name” errors (e.g. WHERE city='Boston' OR 'Chicago').",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have column with MULTIPLE WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have column with MULTIPLE WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 2 column with MULTIPLE WHERE condition", "must have SUB-QUERY"]
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
        characteristics ="Solution query must have OR MULTIPLE CONDITION on the SAME COLUMN (e.g. p.bornCity='Rome' OR p.bornCity='Genoa' this represent one column with MULTIPLE CONDITION). " \
            "The exercise should naturally lead the student to make a mistake which consists in use AND respect to OR " \
            "(e.g. WHERE bornCity='Boston' AND bornCity='Chicago' bornCity must be only one).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table","must have column with OR in MULTIPLE WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have column with OR in MULTIPLE WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 2 column with OR in MULTIPLE WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_40_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION: SqlErrorDetails(#puo essere migliorata?
        description="Tautological or inconsistent expression",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in tautological or inconsistent expression (e.g. start_date > end_date). " \
        "Ask the student to solve a query that has many conditions with operators made on the same variable e.g. price > 10 AND price < 100, age > 18 OR age >= 0, to improuve the learning " \
        "add CHECK at table.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE with CHECK", "must have 2-6 COLUMNS x table", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_41_DISTINCT_IN_SUM_OR_AVG: SqlErrorDetails(
        description="Use DISTINCT into SUM or AVG",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in use DISTINCT inside AVG or SUM. " \
            "The query in solution is mandatory that have many AGGREGATION of type AVG or SUM",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have AVG or SUM AGGREGATION", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 AVG or SUM AGGREGATION", "must have 2 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 AVG or SUM AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    #SEM_42_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES
    SqlErrors.SEM_43_WILDCARDS_WITHOUT_LIKE: SqlErrorDetails(
        description="Wildcards without LIKE",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in forget to use LIKE (ex. name = 'M%'). " \
            "The query in solution is mandatory that have many WHERE condition with use of many WILDCARDS",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have WHERE condition with WILDCARDS"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 WHERE condition with WILDCARDS", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 WHERE condition with WILDCARDS", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_44_INCORRECT_WILDCARD: SqlErrorDetails(
        description="Incorrect wildcard",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in using incorrect wildcard: using _ instead of %." \
        "Creates queries that must include some symbols used in wildcard like +, *, (), [], {}, ^, %, _",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have WHERE condition with WILDCARDS"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 WHERE condition with WILDCARDS", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 WHERE condition with WILDCARDS", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_45_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL: SqlErrorDetails(
        description="Mixing a '> 0' with IS NOT NULL or empty string with NULL",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in Mixing a '> 0' with 'IS NOT NULL' or empty string with 'NULL'. " \
        "In the WHERE must have condition that are NULL or empty string",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_46_NULL_IN_IN_ANY_ALL_SUBQUERY: SqlErrorDetails(
        description="NULL in IN/ANY/ALL subquery",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in return NULL when using IN/ANY/ALL." \
            "In the WHERE must be conditions that use some ANY/ALL/IN key with INSIDE nullable return value.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 1 ANY or ALL or IN in WHERE condition", "must have SUB-QUERY"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 ANY or ALL or IN in WHERE condition", "must have SUB-QUERY"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 ANY or ALL or IN in WHERE condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SEM_49_MANY_DUPLICATES: SqlErrorDetails(
        description="Many duplicates",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in query that returns (or can return) many times the same values " \
        "i.e. a query that doesn't select at least a primary or unique key. The solution must not have UNIQUE KEY IN SELECT, AGGREGATION or GROUP BY",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have DISTINCT", "must have 1 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have DISTINCT", "must have 3 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have DISTINCT", "must have 3 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    # SEM_50_CONSTANT_COLUMN_OUTPUT
    SqlErrors.LOG_52_OR_INSTEAD_OF_AND: SqlErrorDetails(
        description="OR instead of AND",
        characteristics ="Solution query must have more AND CONDITION (e.g. p.film='Alien' AND p.film='Eragon' -> I want both film information from same person id). " \
            "Solution must not have IN format like 'position IN ('Manager', 'Supervisor')' but I want this format 'position ='Manager' AND position = 'Supervisor''" \
            "The exercise should naturally lead the student to make a mistake which consists in use OR respect to AND "
            "(e.g. WHERE p.film='Alien' OR p.film='Eragon' ERROR because I want both information).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_53_EXTRANEOUS_NOT_OPERATOR: SqlErrorDetails( #questo e il successivo sono molto simili
        description="Extraneous NOT operator",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using NOT where it should have not been used." \
        "In the solution must have more NOT to improuve the learning of its use",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 NOT in WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 NOT in WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 NOT in WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_54_MISSING_NOT_OPERATOR: SqlErrorDetails(#questo e il precedente sono molto simili
        description="Missing NOT operator",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in not using NOT where it should have been used." \
        "In the solution must have more NOT to improuve the learning of its use",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 2 NOT in WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 NOT in WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 NOT in WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_55_SUBSTITUTING_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO: SqlErrorDetails(#puo essere migliorata?
        description="Substituting existence negation with <>",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in asking for a value being " \
        "different or NULL instead of checking if it do NOT EXIST (e.g. if we want: list the names of actors who have acted in a movie released in 2015 " \
        "but we do this wrong: list the names of actors who have acted in at least one movie not released in 2015)",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have NOT EXIST in WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have NOT EXIST in WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 2 NOT EXIST in WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_56_PUTTING_NOT_IN_FRONT_OF_INCORRECT_IN_OR_EXISTS: SqlErrorDetails(#puo essere migliorata?
        description="Putting NOT in front of incorrect IN/EXISTS",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in when multiple IN/EXISTS are present, putting NOT on the wrong one " \
        "(e.g. if we want: list the names of actors who have acted in a movie released in 2015; " \
        "but we do this wrong: list the names of actors who have acted in at least one movie but not in a movie that was released in 2015)",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have EXIST in WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have EXIST in WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 2 EXIST in WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),            
    # LOG_56_PUTTING_NOT_IN_FRONT_OF_INCORRECT_IN_OR_EXISTS               
    SqlErrors.LOG_57_INCORRECT_COMPARISON_OPERATOR_OR_VALUE: SqlErrorDetails(
        description="Incorrect comparison operator or incorrect value compared",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using the incorrect comparison operator or " \
        "using the correct operator on a wrong value. In query solution must be more operator usage",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have 1 COMPARISON OPERATOR in WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 COMPARISON OPERATOR in WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 COMPARISON OPERATOR in WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_58_JOIN_ON_INCORRECT_TABLE: SqlErrorDetails(
        description="Join on incorrect table",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in make join operation performed on the correct number of tables, " \
        "but with the wrong tables. In TABLE CREATION must be similar table (e.g. table student and table students_score ) and must have similar column with different meanings " \
        "(e.g. users.name = products.name)",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS x table", "must have JOIN", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 3-4 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 JOIN", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 4-6 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 JOIN", "must have 3 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_59_JOIN_WHEN_JOIN_NEEDS_TO_BE_OMITTED: SqlErrorDetails(
        description="Join when join needs to be omitted",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in performing the join operation on a table not required for the solution. " \
        "In TABLE CREATION must be similar table (e.g. table student and table students_score) and more table that the solution need",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS x table", "must have JOIN", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 3-4 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 JOIN", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 4-6 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 2 JOIN", "must have 3 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_60_JOIN_ON_INCORRECT_COLUMN_MATCHES_POSSIBLE: SqlErrorDetails(
        description="Join on incorrect column (matches possible)",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in performing the join operation on the correct table, " \
        "but using the wrong column (values can still match). In TABLE CREATION must have equal column with different meanings (e.g. users.name = products.name)",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS x table", "must have JOIN", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 3-4 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 JOIN", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 4-6 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 2 JOIN", "must have 3 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_62_MISSING_JOIN: SqlErrorDetails(#puo essere migliorata?
        description="Missing join",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in query does not use a table needed for the solution.",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS x table", "must have JOIN", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 3-4 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 JOIN", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 4-6 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 2 JOIN", "must have 3 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_63_MPROPER_NESTING_OF_EXPRESSIONS: SqlErrorDetails(#non funziona sempre se metto da 3 in poi nested cond. e non gli piaciono le subquery
        description="Improper nesting of expressions",
        characteristics ="Solution query must have multiple condition (NO SUB-QUERY) that must require NESTING (e.g. (condizione1 OR condizione2) AND condizione3 -> " \
        "NESTING are the condition inside parentesis which are mandatory). The exercise should naturally lead the student to make a mistake which consists in " \
        "invalid logic due to parenthesis used in the wrong places (e.g. age > (price > 10) a number cant > of boolean).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS x table", "must have NESTED WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have NESTED WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 2 NESTED WHERE condition", "must have AGGREGATION"] #, "must have SUB-QUERY"
        }
    ),
    SqlErrors.LOG_64_IMPROPER_NESTING_OF_SUBQUERIES: SqlErrorDetails(
        description="Improper nesting of subqueries",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using nested subqueries but they are nested incorrectly." \
        "The solution must have sub-query NOT NESTED",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS x table", "must have WHERE condition", "must have SUB-QUERY NOT NESTED"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS x table", "must have 2 WHERE condition", "must have SUB-QUERY NOT NESTED"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS x table", "must have 3 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY NOT NESTED"]
        }
    ),                       
    # LOG_66_MISSING_EXPRESSION                                           
    # LOG_67_EXPRESSION_ON_INCORRECT_COLUMN                               
    # LOG_68_EXTRANEOUS_EXPRESSION
    # 25-11
    #                                         
    # LOG_69_EXPRESSION_IN_INCORRECT_CLAUSE                               
    # LOG_70_EXTRANEOUS_COLUMN_IN_SELECT                                  
    # LOG_71_MISSING_COLUMN_FROM_SELECT
    # 27-11
    #                                    
    # LOG_72_MISSING_DISTINCT_FROM_SELECT                                 
    # LOG_73_MISSING_AS_FROM_SELECT                                       
    # LOG_74_MISSING_COLUMN_FROM_ORDER_BY
    # 28-11
    #                                  
    # LOG_75_INCORRECT_COLUMN_IN_ORDER_BY                                 
    # LOG_76_EXTRANEOUS_ORDER_BY_CLAUSE                                   
    # LOG_77_INCORRECT_ORDERING_OF_ROWS
    # 2-12
    #                                    
    # LOG_78_DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE          
    # LOG_79_MISSING_DISTINCT_FROM_FUNCTION_PARAMETER                     
    # LOG_80_INCORRECT_FUNCTION
    # 3-12
    #                                            
    # LOG_81_INCORRECT_COLUMN_AS_FUNCTION_PARAMETER
    # COM_83_UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE                        
    # COM_84_UNNECESSARY_JOIN
    # 4-12
    #  
    # COM_86_CORRELATION_NAMES_ARE_ALWAYS_IDENTICAL
    # COM_88_LIKE_WITHOUT_WILDCARDS                                       
    # COM_89_UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY
    # 5-12
    #  
    # COM_91_UNNECESSARY_AGGREGATE_FUNCTION
    # COM_93_UNNECESSARY_ARGUMENT_OF_COUNT
    # COM_95_GROUP_BY_WITH_SINGLETON_GROUPS
    # 6-12
    #                                
    # COM_96_GROUP_BY_WITH_ONLY_A_SINGLE_GROUP                            
    # COM_97_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT                       
    # COM_98_UNION_CAN_BE_REPLACED_BY_OR
    # 8-12
    #                                   
    # COM_99_UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE
    # COM_102_INEFFICIENT_UNION
    # 9-12
    #
    # COM_104_CONDITION_ON_LEFT_TABLE_IN_LEFT_OUTER_JOIN                 
    # COM_105_OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN
    # 10-12

    # 11-12 fare i mancanti
}