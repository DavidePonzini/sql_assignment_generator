# In error_details.py
from dataclasses import dataclass
from .difficulty_level import DifficultyLevel
from sql_error_categorizer.sql_errors import SqlErrors

#inner query gli fa schifo a chatgpt
@dataclass
class SqlErrorDetails:
    description: str
    characteristics: str
    constraints: dict[DifficultyLevel, list[str]]
    
ERROR_DETAILS_MAP ={
    SqlErrors.SYN_2_AMBIGUOUS_COLUMN: SqlErrorDetails(
        description="Ambiguous column",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers SQL error code 42702. " \
            "In table creation must make some column names from different tables the same.",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS per table", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table ", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_4_UNDEFINED_COLUMN: SqlErrorDetails(
        description="Undefined column",
        characteristics = "exercise should naturally tempts student to make a mistake that triggers SQL error code 42703; to cause this, " \
            "it is necessary to make the column name more complex or longer.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 1 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 WHERE condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_7_UNDEFINED_OBJECT: SqlErrorDetails(
        description="Undefined object",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers SQL error code 42704, " \
            "to cause this, it is necessary to make the table name more complex or longer.",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS per table"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have2-6 COLUMNS per table", "must have 2 WHERE condition", "must have SUB-QUERY","must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_8_INVALID_SCHEMA_NAME: SqlErrorDetails(
        description="Invalid schema name",
        characteristics = "It is necessary include the schema name when creating the table in order to produce a student mistake that " \
            "triggers SQL error code 3F000. Create different table of different schema (more than 2 schema)",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS per table", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 3 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SYN_9_MISSPELLINGS: SqlErrorDetails(
        description="Misspellings",
        characteristics ="a query that can cause errors possibly due to typos — for example, by generating tables and COLUMNS with complex names "
        "(students may mistype them) or with very similar names (e.g., name and names). In case with more than 1 CREATE TABLE the solution MUST HAVE " \
        "2 or more similar colums",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 1 COLUMNS per table", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SYN_10_SYNONYMS: SqlErrorDetails(
        description="Synonyms",
        characteristics ="exercise should naturally tempts student to make a mistake because students may misremember the correct name — for example, " \
            "by creating tables and COLUMNS with similar names (like competition and competitor) or similar meanings (like monster and zombie). " \
            "In case with more than 1 CREATE TABLE the solution MUST HAVE 2 or more similar colums",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table",  "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 3-5 COLUMNS per table", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 WHERE condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_11_OMITTING_QUOTES_AROUND_CHARACTER_DATA: SqlErrorDetails(
        description="Omitting quotes around character data",
        characteristics ="exercise should naturally tempts student to make a mistake of the type 'strings not quoted' " \
            "It is mandatory use WHERE clause involving in many condition with STRING variables (e.g. name = 'value').",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 1 WHERE STRING condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 WHERE STRING condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 WHERE STRING condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_12_FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE: SqlErrorDetails( #non funziona sempre se metto da 3 in poi multiple cond.
        description="Failure to specify column name twice",
        characteristics = "Solution query must have MULTIPLE CONDITION on the SAME COLUMN (e.g. p.film='Alien' OR/AND p.film='Superman' this represent one column with MULTIPLE CONDITION). " \
            "Solution must not have IN format like 'position IN ('Manager', 'Supervisor')' but I want this format 'position ='Manager' OR position = 'Supervisor''" \
            "exercise should naturally tempts student to make a mistake that can cause 'miss column name' errors (e.g. WHERE city='Boston' OR 'Chicago').",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have column with MULTIPLE WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have column with MULTIPLE WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 2 column with MULTIPLE WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SYN_15_AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED: SqlErrorDetails(
        description="Grouping error: aggregate functions cannot be nested",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers SQL error code 42803 " \
            "by generating a query in natural language that seems to involve one AGGREGATION inside another " \
            "(e.g. 'the book that has the maximum number of sales' and in database doesn't store the sales count).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 1 AGGREGATION"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have SUB-QUERY", "must have 2 AGGREGATION"]
        }
    ),
    SqlErrors.SYN_19_USING_WHERE_TWICE: SqlErrorDetails(
        description="Using WHERE twice",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers use of multiple WHERE",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 WHERE condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SYN_21_COMPARISON_WITH_NULL: SqlErrorDetails(
        description="Comparison with NULL",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers use of equal (=) in presence of NULL, some column must be nullable",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 WHERE condition", "must have SUB-QUERY", "must have 2 AGGREGATION"]
        }
    ),
    SqlErrors.SYN_26_TOO_MANY_COLUMNS_IN_SUBQUERY: SqlErrorDetails(
        description="Too many COLUMNS in subquery",
        characteristics ="exercise should naturally tempts student to make a mistake which consists in inserting many column in subquery." \
            " The query in solution is mandatory that have subquery to trigger error in student",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 WHERE condition", "must have 2 AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SYN_35_IS_WHERE_NOT_APPLICABLE: SqlErrorDetails(
        description="Use 'IS' where it's not applicable",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in use IS with condition not null (e.g. female IS true)." \
        "The query in solution is mandatory that have many WHERE condition with different type (boolean, integer, string, NULL)",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-4 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_39_AND_INSTEAD_OF_OR: SqlErrorDetails(
        description="AND instead of OR",
        characteristics ="Solution query must have OR MULTIPLE CONDITION on the SAME COLUMN (e.g. p.bornCity='Rome' OR p.bornCity='Genoa' this represent one column with MULTIPLE CONDITION). " \
            "The exercise should naturally lead the student to make a mistake which consists in use AND respect to OR " \
            "(e.g. WHERE bornCity='Boston' AND bornCity='Chicago' bornCity must be only one).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table","must have column with OR in MULTIPLE WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 1 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have column with OR in MULTIPLE WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 2 column with OR in MULTIPLE WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_40_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION: SqlErrorDetails(
        description="Tautological or inconsistent expression",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in tautological or inconsistent expression (e.g. start_date > end_date). " \
        "Solution query must have MULTIPLE CONDITION on the SAME COLUMN (e.g. p.price > 10 AND p.price < 100, p.age < 18 OR p.age >= 0 this represent one column with MULTIPLE CONDITION). " \
        "Add CHECK at table that will be use.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have column with MULTIPLE WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have column with MULTIPLE WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE with CHECK", "must have 2-6 COLUMNS per table", "must have column with MULTIPLE WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_41_DISTINCT_IN_SUM_OR_AVG: SqlErrorDetails(
        description="Use DISTINCT into SUM or AVG",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in use DISTINCT inside AVG or SUM. " \
            "The query in solution is mandatory that have many AGGREGATION of type AVG or SUM",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have AVG or SUM AGGREGATION", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 AVG or SUM AGGREGATION", "must have 2 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 AVG or SUM AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_42_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES: SqlErrorDetails(
        description="DISTINCT that might remove important duplicates",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in removing duplicates when we might want them (e.g. SELECT DISTINCT person.Hobby, " \
        "where a person can have more than one hpbby). The solution must not have DISTINCT, UNIQUE KEY, AGGREGATION or GROUP BY in SELECT clause",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have NO AGGREGATION", "must have NO GROUP BY", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have NO AGGREGATION", "must have NO GROUP BY", "must have 2 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have NO AGGREGATION", "must have NO GROUP BY", "must have 2 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_43_WILDCARDS_WITHOUT_LIKE: SqlErrorDetails(
        description="Wildcards without LIKE",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in forget to use LIKE (ex. name = 'M%'). " \
            "The query in solution is mandatory that have many WHERE condition with use of WILDCARDS",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have WHERE condition with WILDCARDS"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 WHERE condition with WILDCARDS", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 WHERE condition with WILDCARDS", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_44_INCORRECT_WILDCARD: SqlErrorDetails(
        description="Incorrect wildcard",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in using incorrect wildcard: using _ instead of %." \
        "Creates queries that must include some symbols used in wildcard like +, *, (), [], {}, ^, %, _",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have WHERE condition with WILDCARDS"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 WHERE condition with WILDCARDS", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 WHERE condition with WILDCARDS", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_45_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL: SqlErrorDetails(
        description="Mixing a '> 0' with IS NOT NULL or empty string with NULL",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in Mixing a '> 0' with 'IS NOT NULL' or empty string with 'NULL'. " \
        "In the WHERE must have condition that are NULL or empty string",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_46_NULL_IN_IN_ANY_ALL_SUBQUERY: SqlErrorDetails(
        description="NULL in IN/ANY/ALL subquery",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in return NULL when using IN/ANY/ALL." \
            "In the WHERE must be conditions that use some ANY/ALL/IN key with INSIDE nullable return value.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 1 ANY or ALL or IN in WHERE condition", "must have SUB-QUERY"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 ANY or ALL or IN in WHERE condition", "must have SUB-QUERY"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 ANY or ALL or IN in WHERE condition", "must have SUB-QUERY", "must have AGGREGATION"]
        }
    ),
    SqlErrors.SEM_49_MANY_DUPLICATES: SqlErrorDetails(
        description="Many duplicates",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in query that returns (or can return) many times the same values " \
        "i.e. a query that doesn't select at least a primary or unique key. The solution must not have UNIQUE KEY IN SELECT, AGGREGATION or GROUP BY",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have DISTINCT", "must have 1 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have DISTINCT", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have DISTINCT", "must have 3 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.SEM_50_CONSTANT_COLUMN_OUTPUT: SqlErrorDetails(
        description="Constant column output",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in return a single row with constant values usually because of" \
        "query condition or CHECK constraint. The solution must have CHECK in creation table and at least one column in SELECT that is not constant and at least one that is constant in CHECK",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have DISTINCT", "must have 1 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have DISTINCT", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have DISTINCT", "must have 3 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_52_OR_INSTEAD_OF_AND: SqlErrorDetails(
        description="OR instead of AND",
        characteristics ="Solution query must have more AND CONDITION (e.g. p.film='Alien' AND p.film='Eragon' -> I want both film information from same person id). " \
            "Solution must not have IN format like 'position IN ('Manager', 'Supervisor')' but I want this format 'position ='Manager' AND position = 'Supervisor''" \
            "The exercise should naturally lead the student to make a mistake which consists in use OR respect to AND "
            "(e.g. WHERE p.film='Alien' OR p.film='Eragon' ERROR because I want both information).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_53_EXTRANEOUS_NOT_OPERATOR: SqlErrorDetails( #questo e il successivo sono molto simili
        description="Extraneous NOT operator",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using NOT where it should have not been used." \
        "In the solution must have more NOT to improuve the learning of its use",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 NOT in WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 NOT in WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 NOT in WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_54_MISSING_NOT_OPERATOR: SqlErrorDetails(#questo e il precedente sono molto simili
        description="Missing NOT operator",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in not using NOT where it should have been used." \
        "In the solution must have more NOT to improve the learning of its use",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 NOT in WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 NOT in WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 NOT in WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_55_SUBSTITUTING_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO: SqlErrorDetails(#puo essere migliorata?
        description="Substituting existence negation with <>",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in asking for a value being " \
        "different or NULL instead of checking if it do NOT EXIST (e.g. if we want: list the names of actors who have acted in a movie released in 2015 " \
        "but we do this wrong: list the names of actors who have acted in at least one movie not released in 2015)",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have NOT EXIST in WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have NOT EXIST in WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 2 NOT EXIST in WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_56_PUTTING_NOT_IN_FRONT_OF_INCORRECT_IN_OR_EXISTS: SqlErrorDetails(#puo essere migliorata?
        description="Putting NOT in front of incorrect IN/EXISTS",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in when multiple IN/EXISTS are present, putting NOT on the wrong one " \
        "(e.g. if we want: list the names of actors who have acted in a movie released in 2015; " \
        "but we do this wrong: list the names of actors who have acted in at least one movie but not in a movie that was released in 2015)",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have EXIST in WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have EXIST in WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 2 EXIST in WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),            
    SqlErrors.LOG_57_INCORRECT_COMPARISON_OPERATOR_OR_VALUE: SqlErrorDetails(
        description="Incorrect comparison operator or incorrect value compared",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using the incorrect comparison operator or " \
        "using the correct operator on a wrong value. In query solution must be more operator usage",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 1 COMPARISON OPERATOR in WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 COMPARISON OPERATOR in WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 COMPARISON OPERATOR in WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_58_JOIN_ON_INCORRECT_TABLE: SqlErrorDetails(
        description="Join on incorrect table",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in make join operation performed on the correct number of tables, " \
        "but with the wrong tables. In TABLE CREATION must be similar table (e.g. table student and table students_score ) and must have similar column with different meanings " \
        "(e.g. users.name = products.name)",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS per table", "must have JOIN", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 3-4 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 JOIN", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 4-6 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 JOIN", "must have 3 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_59_JOIN_WHEN_JOIN_NEEDS_TO_BE_OMITTED: SqlErrorDetails(
        description="Join when join needs to be omitted",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in performing the join operation on a table not required for the solution. " \
        "In TABLE CREATION must be similar table (e.g. table student and table students_score) and more table that the solution need",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS per table", "must have JOIN", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 3-4 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 JOIN", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 4-6 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 2 JOIN", "must have 3 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_60_JOIN_ON_INCORRECT_COLUMN_MATCHES_POSSIBLE: SqlErrorDetails(
        description="Join on incorrect column (matches possible)",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in performing the join operation on the correct table, " \
        "but using the wrong column (values can still match). In TABLE CREATION must have equal column with different meanings (e.g. users.name = products.name)",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS per table", "must have JOIN", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 3-4 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 JOIN", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 4-6 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 2 JOIN", "must have 3 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_62_MISSING_JOIN: SqlErrorDetails(#puo essere migliorata?
        description="Missing join",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in query does not use a table needed for the solution.",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS per table", "must have JOIN", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 3-4 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 JOIN", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 4-6 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 2 JOIN", "must have 3 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_63_MPROPER_NESTING_OF_EXPRESSIONS: SqlErrorDetails(#non funziona sempre se metto da 2 in poi nested cond.
        description="Improper nesting of expressions",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in invalid logic due to parenthesis used in the wrong places "
        "(e.g. age > (price > 10) a number cant > of boolean). Solution query must have multiple condition that must require NESTING (e.g. (condizione1 OR condizione2) AND condizione3 -> " \
        "NESTING are the condition inside parentesis which are MANDATORY). Cannot use SUB-QUERY",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have NO SUB-QUERY", "must have NESTED WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have NO SUB-QUERY", "must have 2 NESTED WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have NO SUB-QUERY", "must have 2 NESTED WHERE condition", "must have AGGREGATION"]
        }
    ),
    SqlErrors.LOG_64_IMPROPER_NESTING_OF_SUBQUERIES: SqlErrorDetails(
        description="Improper nesting of subqueries",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using nested subqueries but they are nested incorrectly." \
        "The solution must have sub-query NOT NESTED",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "must have 2 COLUMNS per table", "must have WHERE condition", "must have SUB-QUERY NOT NESTED"],
            DifficultyLevel.MEDIUM: ["must have 2-3 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 WHERE condition", "must have SUB-QUERY NOT NESTED"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY NOT NESTED"]
        }
    ),
    SqlErrors.LOG_66_MISSING_EXPRESSION: SqlErrorDetails(
        description="Missing expression",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in miss a required expression altering the correct logic." \
        "The request in natural language must contain ambiguity: some information required for the query should be left out or implied, so the student can easily misunderstand it.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_67_EXPRESSION_ON_INCORRECT_COLUMN: SqlErrorDetails(
        description="Expression on incorrect column",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in a required expression which is present but on the wrong column." \
        "Solution query must have similar condition e.g. SELECT * FROM store s1, store s2 WHERE s1.value = 100 AND s2.value <> 100" \
        "The request in natural language must contain ambiguity: some information required for the query should be left out or implied, so the student can easily misunderstand it.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_68_EXTRANEOUS_EXPRESSION: SqlErrorDetails(
        description="Extraneous expression",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in an extraneous expression which changes the correct logic." \
        "The request in natural language must contain ambiguity: must include an over-detailed explanation with entity names that resemble table names, encouraging the student " \
        "to think an additional condition or table is needed when in fact it is not.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_69_EXPRESSION_IN_INCORRECT_CLAUSE: SqlErrorDetails(
        description="Expression in incorrect clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in insert an expression in incorrect clause "\
        "(e.g. using HAVING clause instead of WHERE or WHERE instead HAVING). You need to create deliverables that appear to say one thing, but technically imply another "\
        "(e.g. Show all products priced at more than €50 - price>50 inserted in HAVING and not in WHERE).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE OR HAVING condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE OR HAVING condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE OR HAVING condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_70_EXTRANEOUS_COLUMN_IN_SELECT: SqlErrorDetails(
        description="Extraneous column in SELECT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in include in SELECT a column which has not been asked for. " \
        "The natural language query must be ambiguous, so that some columns in the solution query's SELECT statement can be identified as required when they are not.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_71_MISSING_COLUMN_FROM_SELECT: SqlErrorDetails(
        description="Missing column from SELECT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in omit in SELECT a column which has been asked for. " \
        "The natural language query must be ambiguous and must require returning many columns in SELECT statement, so that some columns may not be added by forgetfulness.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_72_MISSING_DISTINCT_FROM_SELECT: SqlErrorDetails(
        description="Missing DISTINCT from SELECT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in SELECT doesn't have DISTINCT when DISTINCT is required in the solution. " \
        "The natural language query must require the use of DISTINCT for some column.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have DISTINCT", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have DISTINCT", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have DISTINCT", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_73_MISSING_AS_FROM_SELECT: SqlErrorDetails(
        description="Missing AS from SELECT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in the correct column is selected but has not been renamed as asked. " \
        "The natural language query must ask to rename all column in SELECT.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_74_MISSING_COLUMN_FROM_ORDER_BY: SqlErrorDetails(
        description="Missing column from ORDER BY clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in results which have not ordered on a requested columns. " \
        "The natural language query must INDIRECTLY define the order in which return the result table, that the student will insert into ORDER BY.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have ORDER BY", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have  2 columns in ORDER BY", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 columns in ORDER BY", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_75_INCORRECT_COLUMN_IN_ORDER_BY: SqlErrorDetails(
        description="Incorrect column in ORDER BY clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in results have been ordered on the wrong colums. " \
        "The natural language query must INDIRECTLY define the order in which return the result table, that the student will insert into ORDER BY.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have ORDER BY", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 columns in ORDER BY", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 columns in ORDER BY", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_76_EXTRANEOUS_ORDER_BY_CLAUSE: SqlErrorDetails(
        description="Extraneous ORDER BY clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in results have been ordered when they were not required to. " \
        "The natural language query must make it appear that a column order in the resulting table is needed but it is not required.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have NO ORDER BY", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have NO ORDER BY", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have NO ORDER BY", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),     
    SqlErrors.LOG_77_INCORRECT_ORDERING_OF_ROWS: SqlErrorDetails(
        description="Incorrect ordering of rows",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in results ordered in not requested way (e.g. ASC onstead of DESC). " \
        "The natural language query must be ambiguous, not making the order of the columns clear and simple.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have ORDER BY", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 columns in ORDER BY", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 columns in ORDER BY", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_78_DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE: SqlErrorDetails(
        description="DISTINCT as function parameter where not applicable",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in use DISTINCT where it should not be used "
        "(e.g. COUNT(DISTINCT zip) where zip is a primary key). In the natural language query return many unique column or column which not require use of DISTINCT",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_79_MISSING_DISTINCT_FROM_FUNCTION_PARAMETER: SqlErrorDetails(
        description="Missing DISTINCT from function parameter",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in not use DISTINCT in a function when it should have " \
        "(e.g COUNT(column) instead of COUNT(DISTINCT column)). In the natural language query return column which require use of DISTINCT but NOT with UNIQUE values",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have DISTINCT", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have DISTINCT", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have DISTINCT", "must have 4 WHERE condition", "must have AGGREGATION", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_80_INCORRECT_FUNCTION: SqlErrorDetails(
        description="Incorrect function",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in the wrong aggregate function has been used (e.g. SUM instead of AVG). " \
            "The natural language query must be ambiguous to confuse the use of aggregate functions respect others (e.g. total can be SUM or COUNT).",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have AGGREGATION", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 AGGREGATION", "must have 3 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 AGGREGATION", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.LOG_81_INCORRECT_COLUMN_AS_FUNCTION_PARAMETER: SqlErrorDetails(#puo essere migliorata?
        description="Incorrect column as function parameter",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in call function on the wrong column "
        "(e.g. EXTRACT(month FROM ts_start) instead of EXTRACT(month FROM ts_end)). The natural language query must be ambiguous to confuse the student in the choice " \
        "of columns that go into the functions.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have AGGREGATION", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 AGGREGATION", "must have 3 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 3 AGGREGATION", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_83_UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE: SqlErrorDetails(
        description="Unnecessary DISTINCT in SELECT clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in SELECT which includes DISTINCT when it's not needed" \
        "(e.g. when we do select of a primary key that already return unique values). In solution there must be no DISTINCT.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have AGGREGATION", "must have 3 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have AGGREGATION", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_84_UNNECESSARY_JOIN: SqlErrorDetails(#puo essere migliorata?
        description="Unnecessary join",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in a table is joined even though only its PK is accessed "
        "(which we already have as FK). The solution in SELECT must have foreign keys to a table that are not used in joins.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have AGGREGATION", "must have 3 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have AGGREGATION", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_86_CORRELATION_NAMES_ARE_ALWAYS_IDENTICAL: SqlErrorDetails(#non funziona- manca costraint in tesi #########################################################################
        description="Correlation names are always identical",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in two tables always have the same data, because their PKs are equated " \
        "and same alias as table. In the assignment create two table with same PRIMARY KEY (e.g. table player with PK player_id and table player_info with PK player_id).",
        constraints={
            DifficultyLevel.EASY: ["must have 2 CREATE TABLE", "2 CREATE TABLE must have same PK", "must have 2 COLUMNS per table", "must have 2 WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "2 CREATE TABLE must have same PK", "must have 2-4 COLUMNS per table", "must have AGGREGATION", "must have 3 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "2 CREATE TABLE must have same PK", "must have 2-6 COLUMNS per table", "must have AGGREGATION", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),                         
    SqlErrors.COM_88_LIKE_WITHOUT_WILDCARDS: SqlErrorDetails(
        description="LIKE without wildcards",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using LIKE without any wildcards is the same wrong as using =. " \
        "The natural language query you must confuse the student by making him believe that the LIKE keyword is necessary. In the solution MUST NOT HAVE LIKE and WILDCARDS.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have WHERE condition without WILDCARDS"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have AGGREGATION", "must have 2 WHERE condition without WILDCARDS"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have AGGREGATION", "must have 3 WHERE condition without WILDCARDS", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_89_UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY: SqlErrorDetails(
        description="Unnecessarily complicated SELECT in EXISTS subquery",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using more than one column in the SELECT clause " \
        "of an EXISTS subquery. In the solution must be EXISTS WITH only one column in SELECT and WITHOUT DISTINCT.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have EXIST in WHERE condition", "must have SUB-QUERY"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 2 EXIST in WHERE condition", "must 2 have SUB-QUERY"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have AGGREGATION", "must have 3 EXIST in WHERE condition", "must 3 have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_91_UNNECESSARY_AGGREGATE_FUNCTION: SqlErrorDetails(
        description="Unnecessary aggregate function",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using an aggregation function on a single value when it isn't necessary "
        "(e.g. (SELECT MAX(SAL) FROM EMP GROUP BY SAL) which is the same as (SELECT DISTINCT SAL FROM EMP)). In natural language query use term as 'maximum', 'minimum', " \
        "'count', 'average' ecc... that help to confuse the student but NOT use AGGREGATION.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have NO AGGREGATION", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have NO AGGREGATION", "must have 2 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have NO AGGREGATION", "must have 3 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_93_UNNECESSARY_ARGUMENT_OF_COUNT: SqlErrorDetails(
        description="Unnecessary argument of COUNT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using COUNT(column) instead of COUNT(*) when the column " \
        "cannot have NULL values. In solution must be the aggregation count with a star -> COUNT(*) .",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have AGGREGATION", "must have WHERE condition", "must have SUB-QUERY"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have AGGREGATION", "must have 2 WHERE condition", "must 2 have SUB-QUERY"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have AGGREGATION", "must have 3 WHERE condition", "must 3 have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_95_GROUP_BY_WITH_SINGLETON_GROUPS: SqlErrorDetails(
        description="GROUP BY with singleton groups",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using GROUP BY when each group already consists of a single row " \
        "(e.g. GROUP BY id). The solution MUST HAVE GROUP BY but on NON UNIQUE columns",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have NO AGGREGATION", "must have GROUP BY", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have NO AGGREGATION", "must have GROUP BY", "must have 3 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have NO AGGREGATION", "must have GROUP BY", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_96_GROUP_BY_WITH_ONLY_A_SINGLE_GROUP: SqlErrorDetails(
        description="GROUP BY with only a single group",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in use grouping on a column which contains the same value for all rows (e.g. " \
        "SELECT job, COUNT(*) FROM t WHERE job = 'manager' GROUP BY job). The solution must have in select ONLY aggregate functions.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have NO GROUP BY", "must have AGGREGATION", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have NO GROUP BY", "must have 2 AGGREGATION", "must have 3 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have NO GROUP BY", "must have 3 AGGREGATION", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_97_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT: SqlErrorDetails(#controllare
        description="GROUP BY can be replaced with DISTINCT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using GROUP BY when DISTINCT would suffice (e.g. SELECT DISTINCT col1, col2 FROM t instead of " \
        "SELECT col1, col2 FROM t GROUP BY col1, col2). In natural language query must create a query tahat can be solved with DISTINCT but the student can be confused to use GROUP BY.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have NO GROUP BY", "must have DISTINCT", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have NO GROUP BY", "must have DISTINCT", "must have 3 WHERE condition"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have NO GROUP BY", "must have DISTINCT", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_98_UNION_CAN_BE_REPLACED_BY_OR: SqlErrorDetails(#controllare
        description="UNION can be replaced by OR",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in use UNION with two queries with: SAME tables in FROM, SAME column in SELECT and " \
        "mutually exclusive condition. The natural language query must have a request that can be solved with a single SELECT with OR in where condition or with UNION",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have NO UNION", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have NO UNION", "must have 3 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have NO UNION", "must have 4 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_99_UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE: SqlErrorDetails(
        description="Unnecessary column in ORDER BY clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in ordering the results by 2 column where one is functional depending on the other " \
        "(e.g. ORDER BY id_student, student_name). In natural language query MUST BE AMBIGUOUS on the order of the result table in ORDER BY clause, dont use the world 'Sort' or 'Order'.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have 2 columns in ORDER BY", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have 3 columns in ORDER BY", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 4 columns in ORDER BY", "must have 3 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_102_INEFFICIENT_UNION: SqlErrorDetails(
        description="Inefficient UNION",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using UNION instead of UNION ALL with two queries that are always disjoint or " \
        "don't return duplicates. In the natural language query you need to create a case where use of UNION ALL or UNION should be used depending on what request is made. In solution " \
        "if table in FROM are the same MUST USE UNION ALL, else if tables are different MUST USE UNION.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have UNION or UNION ALL", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have UNION or UNION ALL", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have UNION or UNION ALL", "must have 3 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_104_CONDITION_ON_LEFT_TABLE_IN_LEFT_OUTER_JOIN: SqlErrorDetails(
        description="Condition on left table in LEFT OUTER JOIN",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using an ON condition on the LEFT table of an OUTER JOIN " \
        "instead of a condition on WHERE. The natural language query must create ambiguity about which table the condition applies to.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have LEFT OUTHER JOIN", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have LEFT OUTHER JOIN", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 2 LEFT OUTHER JOIN", "must have 3 WHERE condition", "must have SUB-QUERY"]
        }
    ),
    SqlErrors.COM_105_OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN: SqlErrorDetails(#controllare
        description="OUTER JOIN can be replaced by INNER JOIN",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using a WHERE condition on the RIGHT table of an OUTER JOIN " \
        "instead of a condition on ON, making this equivalent to an INNER JOIN. In the solution must be INNER JOIN. The natural language query must create ambiguity about which JOIN " \
        "to use with words like 'right' and 'left'.",
        constraints={
            DifficultyLevel.EASY: ["must have 1 CREATE TABLE", "must have 2 COLUMNS per table", "must have JOIN", "must have WHERE condition"],
            DifficultyLevel.MEDIUM: ["must have 2 CREATE TABLE", "must have 2-4 COLUMNS per table", "must have JOIN", "must have 2 WHERE condition", "must have AGGREGATION"],
            DifficultyLevel.HARD: ["must have 3-5 CREATE TABLE", "must have 2-6 COLUMNS per table", "must have 2 JOIN", "must have 3 WHERE condition", "must have SUB-QUERY"]
        }
    )
}