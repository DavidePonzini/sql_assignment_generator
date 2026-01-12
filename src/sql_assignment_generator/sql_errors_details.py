'''Descriptions and constraints for each supported SQL error.'''

# In error_details.py
from dataclasses import dataclass
from .difficulty_level import DifficultyLevel
from sql_error_categorizer.sql_errors import SqlErrors
from . import constraints

#inner query gli fa schifo a chatgpt
@dataclass
class SqlErrorDetails:
    '''Details about a specific SQL error, including description, characteristics, and constraints.'''
    description: str
    characteristics: str
    constraints: dict[DifficultyLevel, list[constraints.BaseConstraint]]
    
ERROR_DETAILS_MAP = {
    SqlErrors.SYN_2_AMBIGUOUS_COLUMN: SqlErrorDetails(
        description="Ambiguous column",
        characteristics ="exercise should naturally tempts student to make a mistake which consist in table or table alias that are not specified " \
        "for a column present in both (e.g. SELECT A FROM T1, T2 WHERE T1.A = T2.A - forgot in select T1.A). In table creation must make some column names " \
        "from different tables the same.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_4_UNDEFINED_COLUMN: SqlErrorDetails(
        description="Undefined column",
        characteristics = "exercise should naturally tempts student to make a mistake which consist in reference to a column that does not exist " \
        "It is necessary to make the column name more complex or longer.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_7_UNDEFINED_OBJECT: SqlErrorDetails(
        description="Undefined object",
        characteristics ="exercise should naturally tempts student to make a mistake which consist in reference to object that does not exist "
        "(e.g. SELECT * FROM player where table name is Players). In solution is necessary to make the table name more complex or longer.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_8_INVALID_SCHEMA_NAME: SqlErrorDetails(
        description="Invalid schema name",
        characteristics = "It is necessary include the schema name when creating the table in order to produce a student mistake which consist in " \
        "a query that references a schema that does not exist (e.g. SELECT * FROM table.value - where table do not exist). " \
        "Create different table of different schema (more than 2 schema)",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_9_MISSPELLINGS: SqlErrorDetails(
        description="Misspellings",
        characteristics ="a query that can cause errors possibly due to typos — for example, by generating tables and COLUMNS with complex names "
        "(students may mistype them) or with very similar names (e.g., name and names). In case with more than 1 CREATE TABLE the solution MUST HAVE " \
        "2 or more similar colums",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_10_SYNONYMS: SqlErrorDetails(
        description="Synonyms",
        characteristics ="exercise should naturally tempts student to make a mistake because students may misremember the correct name — for example, " \
            "by creating tables and COLUMNS with similar names (like competition and competitor) or similar meanings (like monster and zombie). " \
            "In case with more than 1 CREATE TABLE the solution MUST HAVE 2 or more similar colums",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_11_OMITTING_QUOTES_AROUND_CHARACTER_DATA: SqlErrorDetails(
        description="Omitting quotes around character data",
        characteristics ="exercise should naturally tempts student to make a mistake of the type 'strings not quoted' " \
            "It is mandatory use WHERE clause involving in many condition with STRING variables (e.g. name = 'value').",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type = "STRING")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type = "STRING"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type = "STRING"),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_12_FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE: SqlErrorDetails(
        description="Failure to specify column name twice",
        characteristics = "Solution query must have MULTIPLE CONDITION on the SAME COLUMN (e.g. p.film='Alien' OR p.film='Superman' this represent one column with MULTIPLE CONDITION). " \
            "Solution must not have IN format like 'position IN ('Manager', 'Supervisor')' but I want this format 'position ='Manager' OR position = 'Supervisor''" \
            "exercise should naturally tempts student to make a mistake that can cause 'miss column name' errors (e.g. WHERE city='Boston' OR 'Chicago').",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type = "MULTIPLE")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type = "MULTIPLE"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type = "MULTIPLE"),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }#non funziona sempre se metto da 3 in poi multiple condition
    ),
    SqlErrors.SYN_15_AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED: SqlErrorDetails(
        description="Grouping error: aggregate functions cannot be nested",
        characteristics ="exercise should naturally tempts student to make a mistake that consist in using an aggregate " \
        "function inside an aggregate function. Generate a query in natural language that seems to involve one AGGREGATION " \
        "inside another (e.g. 'the book that has the maximum number of sales' and in database doesn't store the sales count).",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.HasAggregationConstraint(1, state=True)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(2, state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(2, state=True)
            ]
        }
    ),
    SqlErrors.SYN_19_USING_WHERE_TWICE: SqlErrorDetails(
        description="Using WHERE twice",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers use of multiple WHERE",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(2, state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True),
            ]
        }
    ),
    SqlErrors.SYN_21_COMPARISON_WITH_NULL: SqlErrorDetails(
        description="Comparison with NULL",
        characteristics ="exercise should naturally tempts student to make a mistake that triggers use of equal (=) in presence of NULL, some column must be nullable",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(2, state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_26_TOO_MANY_COLUMNS_IN_SUBQUERY: SqlErrorDetails(
        description="Too many COLUMNS in subquery",
        characteristics ="exercise should naturally tempts student to make a mistake which consists in inserting many column in subquery." \
            " The query in solution is mandatory that have subquery to trigger error in student",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.HasSubQueryConstraint(state=True),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(2, state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_35_IS_WHERE_NOT_APPLICABLE: SqlErrorDetails(
        description="Use 'IS' where it's not applicable",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in use IS with condition not null (e.g. female IS true)." \
        "The query in solution is mandatory that have many WHERE condition with different type (boolean, integer, string, NULL)",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(2, state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SEM_39_AND_INSTEAD_OF_OR: SqlErrorDetails(
        description="AND instead of OR",
        characteristics ="Solution query must have OR MULTIPLE CONDITION on the SAME COLUMN (e.g. p.bornCity='Rome' OR p.bornCity='Genoa' " \
        "this represent one column with MULTIPLE CONDITION). The exercise should naturally lead the student to make a mistake which consists "
        "in use AND respect to OR (e.g. WHERE bornCity='Boston' AND bornCity='Chicago' bornCity must be only one).",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type="MULTIPLE"),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(1, type="MULTIPLE"),
                constraints.query.HasAggregationConstraint(2, state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type="MULTIPLE"),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SEM_40_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION: SqlErrorDetails(
        description="Tautological or inconsistent expression",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in tautological "
        "or inconsistent expression (e.g. start_date > end_date). Solution query must have MULTIPLE CONDITION on the SAME COLUMN "
        "(e.g. p.age < 18 OR p.age >= 0 this represent one column with MULTIPLE CONDITION). Add CHECK at table that will be use.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.schema.HasCheckConstraint(1),
                constraints.query.HasWhereConstraint(1, type="MULTIPLE")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.schema.HasCheckConstraint(2),
                constraints.query.HasWhereConstraint(1, type="MULTIPLE"),
                constraints.query.HasAggregationConstraint(2, state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.schema.HasCheckConstraint(3),
                constraints.query.HasWhereConstraint(2, type="MULTIPLE"),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SEM_41_DISTINCT_IN_SUM_OR_AVG: SqlErrorDetails(
        description="Use DISTINCT into SUM or AVG",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in use DISTINCT inside AVG or SUM. " \
            "The query in solution is mandatory that have many AGGREGATION of type AVG or SUM",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.HasAggregationConstraint(2, type=["SUM", "AVG"], state=True)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(2, type=["SUM", "AVG"], state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(2, type=["SUM", "AVG"], state=True)
            ]
        }
    ),
    SqlErrors.SEM_42_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES: SqlErrorDetails(#provare piu volte
        description="DISTINCT that might remove important duplicates",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in removing duplicates when we might want them "
        "(e.g. SELECT DISTINCT person.Hobby, where a person can have more than one hobby). The solution must not have DISTINCT, UNIQUE KEY, AGGREGATION "
        "in SELECT clause and must not have GROUP BY clause.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.HasAggregationConstraint(state=False),
                constraints.query.HasGroupByConstraint(state=False),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="DISTINCT"),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="UK")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=False),
                constraints.query.HasGroupByConstraint(state=False),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="DISTINCT"),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="UK")
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=False),
                constraints.query.HasGroupByConstraint(state=False),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="DISTINCT"),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="UK")
            ]
        }
    ),
    SqlErrors.SEM_43_WILDCARDS_WITHOUT_LIKE: SqlErrorDetails(
        description="Wildcards without LIKE",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in forget to use LIKE (ex. name = 'M%'). " \
            "The query in solution is mandatory that have many WHERE condition with use of WILDCARDS",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type="WILDCARD")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type="WILDCARD"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type="WILDCARD"),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SEM_44_INCORRECT_WILDCARD: SqlErrorDetails(
        description="Incorrect wildcard",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in using incorrect wildcard: using _ instead of %." \
        "Creates queries that must include some symbols used in wildcard like +, *, (), [], {}, ^, %, _",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type="WILDCARD")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type="WILDCARD"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type="WILDCARD"),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SEM_45_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL: SqlErrorDetails(
        description="Mixing a '> 0' with IS NOT NULL or empty string with NULL",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in Mixing a '> 0' with 'IS NOT NULL' or empty string with 'IS NULL'. " \
        "In the WHERE must have condition that are NULL or empty string",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type="NULL/EMPTY")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type="NULL/EMPTY"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type="NULL/EMPTY"),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SEM_46_NULL_IN_IN_ANY_ALL_SUBQUERY: SqlErrorDetails(
        description="NULL in IN/ANY/ALL subquery",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in return NULL when using ANY/ALL/IN." \
            "In the WHERE must be conditions that use some ANY/ALL/IN key with INSIDE nullable return value.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type="ANY/ALL/IN"),
                constraints.query.HasSubQueryConstraint(state=True)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type="ANY/ALL/IN"),
                constraints.query.HasSubQueryConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type="ANY/ALL/IN"),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SEM_49_MANY_DUPLICATES: SqlErrorDetails(#provare piu volte
        description="Many duplicates",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in query that returns (or can return) many times the same values " \
        "i.e. a query that doesn't select at least a primary or unique key. The solution must have UNIQUE KEY or DISTINCT in SELECT",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT/UK")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT/UK"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT/UK"),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SEM_50_CONSTANT_COLUMN_OUTPUT: SqlErrorDetails(
        description="Constant column output",
        characteristics ="the exercise should naturally lead the student to make a mistake which consists in return a single row " \
        "with constant values usually because ofquery condition or CHECK constraint. The solution must have CHECK in creation table " \
        "and at least one column in SELECT that is not constant and at least one that is constant in CHECK",
        constraints={
            DifficultyLevel.EASY: [
                constraints.schema.HasCheckConstraint(1),
                constraints.query.HasWhereConstraint(1)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.schema.HasCheckConstraint(1),
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.schema.HasCheckConstraint(1),
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_52_OR_INSTEAD_OF_AND: SqlErrorDetails(
        description="OR instead of AND",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in use OR respect to AND "
            "(e.g. WHERE p.film='Eragon' OR p.type='Fantasy' ERROR because I want both information)." \
            "Solution query must have more AND CONDITION (e.g. p.film='Eragon' AND p.type='Fantasy'. "
            ,
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_53_EXTRANEOUS_NOT_OPERATOR: SqlErrorDetails(
        description="Extraneous NOT operator",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using NOT " \
        "where it should have not been used. In the solution must have more NOT to improuve the learning of its use",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type="NOT"),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type="NOT"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type="NOT"),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_54_MISSING_NOT_OPERATOR: SqlErrorDetails(
        description="Missing NOT operator",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in not using NOT where " \
        "it should have been used. In the solution must have more NOT to improve the learning of its use. Must have more WHERE condition.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type="NOT"),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type="NOT"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type="NOT"),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_55_SUBSTITUTING_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO: SqlErrorDetails(
        description="Substituting existence negation with <>",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in asking for a value being " \
        "different or NULL instead of checking if it do NOT EXIST (e.g. if we want: list the names of actors who have acted in a movie released in 2015 " \
        "but we do this wrong: list the names of actors who have acted in at least one movie not released in 2015)",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type="NOT EXIST"),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type="NOT EXIST"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type="NOT EXIST"),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_56_PUTTING_NOT_IN_FRONT_OF_INCORRECT_IN_OR_EXISTS: SqlErrorDetails(
        description="Putting NOT in front of incorrect IN/EXISTS",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in when MULTIPLE EXISTS/IN " \
        "are present, putting NOT on the wrong one (e.g. if we want: list the names of actors who have acted in a movie released in 2015; " \
        "but we do this wrong: list the names of actors who have acted in at least one movie but not in a movie that was released in 2015)",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(type="EXIST/NOT EXIST or IN/NOT IN"),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(type="EXIST/NOT EXIST or IN/NOT IN"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type="EXIST/NOT EXIST or IN/NOT IN"),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),            
    SqlErrors.LOG_57_INCORRECT_COMPARISON_OPERATOR_OR_VALUE: SqlErrorDetails(
        description="Incorrect comparison operator or incorrect value compared",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using the incorrect comparison operator or " \
        "using the correct operator on a wrong value. In query solution must be more operator usage",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2, type="COMPARISON OPERATORS"),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type="COMPARISON OPERATORS"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type="COMPARISON OPERATORS"),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_58_JOIN_ON_INCORRECT_TABLE: SqlErrorDetails(
        description="Join on incorrect table",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in make join operation performed on the correct number of tables, " \
        "but with the wrong tables. In TABLE CREATION must be similar table (e.g. table student and table students_score ) and must have similar column with different meanings " \
        "(e.g. users.name = products.name)",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasJoinConstraint(1)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasJoinConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasJoinConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_59_JOIN_WHEN_JOIN_NEEDS_TO_BE_OMITTED: SqlErrorDetails(
        description="Join when join needs to be omitted",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in performing " \
        "the join operation on a table not required for the solution. In TABLE CREATION must be similar table (e.g. table student " \
        "and table students_score) and more table that the solution need",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasJoinConstraint(1)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasJoinConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasJoinConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_60_JOIN_ON_INCORRECT_COLUMN_MATCHES_POSSIBLE: SqlErrorDetails(
        description="Join on incorrect column (matches possible)",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in performing the join operation on the correct table, " \
        "but using the wrong column (values can still match). In TABLE CREATION must have equal column with different meanings (e.g. users.name = products.name)",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasJoinConstraint(1)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasJoinConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasJoinConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_62_MISSING_JOIN: SqlErrorDetails(#puo essere migliorata?
        description="Missing join",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in " \
        "query does not use a table needed for the solution. The exercise MUST have table names almost the same " \
        "to confuse the student in the table choise",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasJoinConstraint(1)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasJoinConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasJoinConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_63_MPROPER_NESTING_OF_EXPRESSIONS: SqlErrorDetails( #puo essere migliorata?
        description="Improper nesting of expressions",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in " \
        "invalid logic due to parenthesis used in the wrong places (e.g. age > (price > 10) a number cant > of boolean). " \
        "Solution query must have multiple condition that must require NESTING (e.g. (condizione1 OR condizione2) AND condizione3 -> " \
        "NESTING are the condition inside parentesis which are MANDATORY). Cannot use SUB-QUERY",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type="NESTED"),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type="NESTED"),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type="NESTED"),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }#non funziona sempre se metto da 2 in poi nested cond.
    ),
    SqlErrors.LOG_64_IMPROPER_NESTING_OF_SUBQUERIES: SqlErrorDetails( #puo essere migliorata?
        description="Improper nesting of subqueries",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using nested subqueries but they are nested incorrectly." \
        "The natural language solution must confuse student to use nested subquery that are not necessary. Solution must have sub-query NOT NESTED",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.HasSubQueryConstraint(type="NOT NESTED"),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(type="NOT NESTED")
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(type="NOT NESTED"),
                constraints.query.HasAggregationConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_66_MISSING_EXPRESSION: SqlErrorDetails(
        description="Missing expression",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in miss a required " \
        "expression altering the correct logic. The request in natural language must contain ambiguity: some information required " \
        "for the query should be left out or implied, so the student can easily misunderstand it.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint()
            ]
        }
    ),
    SqlErrors.LOG_67_EXPRESSION_ON_INCORRECT_COLUMN: SqlErrorDetails(
        description="Expression on incorrect column",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in a required expression which is present but on the wrong column." \
        "Solution query must have similar condition e.g. SELECT * FROM store s1, store s2 WHERE s1.value = 100 AND s2.value <> 100" \
        "The request in natural language must contain ambiguity: some information required for the query should be left out or implied, so the student can easily misunderstand it.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint()
            ]
        }
    ),
    SqlErrors.LOG_68_EXTRANEOUS_EXPRESSION: SqlErrorDetails(
        description="Extraneous expression",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in an extraneous expression which changes the correct logic." \
        "The request in natural language must contain ambiguity: must include an over-detailed explanation with entity names that resemble table names, encouraging the student " \
        "to think an additional condition or table is needed when in fact it is not.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint()
            ]
        }
    ),
    SqlErrors.LOG_69_EXPRESSION_IN_INCORRECT_CLAUSE: SqlErrorDetails(
        description="Expression in incorrect clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in insert an expression in incorrect clause "\
        "(e.g. using HAVING clause instead of WHERE or WHERE instead HAVING). You need to create deliverables that appear to say one thing, but technically imply another "\
        "(e.g. Show all products priced at more than €50 - price>50 inserted in HAVING and not in WHERE).",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2, type="HAVING"),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3, type="HAVING"),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4, type="HAVING"),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint()
            ]
        }
    ),
    SqlErrors.LOG_70_EXTRANEOUS_COLUMN_IN_SELECT: SqlErrorDetails(
        description="Extraneous column in SELECT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in include in SELECT a column which has not been asked for. " \
        "The natural language query must be ambiguous, so that some columns in the solution query's SELECT statement can be identified as required when they are not.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint()
            ]
        }
    ),
    SqlErrors.LOG_71_MISSING_COLUMN_FROM_SELECT: SqlErrorDetails(
        description="Missing column from SELECT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in omit in SELECT a column which has been asked for. " \
        "The natural language query must be ambiguous and must require returning many columns in SELECT statement, so that some columns may not be added by forgetfulness.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint()
            ]
        }
    ),
    SqlErrors.LOG_72_MISSING_DISTINCT_FROM_SELECT: SqlErrorDetails(
        description="Missing DISTINCT from SELECT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in SELECT doesn't have DISTINCT when DISTINCT is required in the solution. " \
        "The natural language query must require the use of DISTINCT for some column.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT")
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT")
            ]
        }
    ),
    SqlErrors.LOG_73_MISSING_AS_FROM_SELECT: SqlErrorDetails(
        description="Missing AS from SELECT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in the correct column is selected but has not been renamed as asked. " \
        "The natural language query must ask to rename all column in SELECT.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint()
            ]
        }
    ),
    SqlErrors.LOG_74_MISSING_COLUMN_FROM_ORDER_BY: SqlErrorDetails(
        description="Missing column from ORDER BY clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in results which have not ordered on a requested columns. " \
        "The natural language query must INDIRECTLY define the order in which return the result table, that the student will insert into ORDER BY.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasOrderByConstraint(1)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasOrderByConstraint(2)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(),
                constraints.query.HasOrderByConstraint(3)
            ]
        }
    ),
    SqlErrors.LOG_75_INCORRECT_COLUMN_IN_ORDER_BY: SqlErrorDetails(
        description="Incorrect column in ORDER BY clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in results have been ordered on the wrong colums. " \
        "The natural language query must INDIRECTLY define the order in which return the result table, that the student will insert into ORDER BY.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasOrderByConstraint(1)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasOrderByConstraint(2)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(),
                constraints.query.HasOrderByConstraint(3)
            ]
        }
    ),
    SqlErrors.LOG_76_EXTRANEOUS_ORDER_BY_CLAUSE: SqlErrorDetails(
        description="Extraneous ORDER BY clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in results have been ordered when they were not required to. " \
        "The natural language query must make it appear that a column order in the resulting table is needed but it is not required.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasOrderByConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasOrderByConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasOrderByConstraint(state=False)
            ]
        }
    ),     
    SqlErrors.LOG_77_INCORRECT_ORDERING_OF_ROWS: SqlErrorDetails(
        description="Incorrect ordering of rows",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in results ordered in not requested way (e.g. ASC onstead of DESC). " \
        "The natural language query must be ambiguous, not making the order of the columns clear and simple.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasOrderByConstraint()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasOrderByConstraint(2)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasOrderByConstraint(3)
            ]
        }
    ),
    SqlErrors.LOG_78_DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE: SqlErrorDetails(
        description="DISTINCT as function parameter where not applicable",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in use DISTINCT where it should not be used "
        "(e.g. COUNT(DISTINCT zip) where zip is a primary key). In the natural language query return many unique column or column which not require use of DISTINCT",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="DISTINCT")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="DISTINCT")
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="DISTINCT")
            ]
        }
    ),
    SqlErrors.LOG_79_MISSING_DISTINCT_FROM_FUNCTION_PARAMETER: SqlErrorDetails(
        description="Missing DISTINCT from function parameter",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in not use DISTINCT in a function when it should have " \
        "(e.g COUNT(column) instead of COUNT(DISTINCT column)). In the natural language query return column which require use of DISTINCT but NOT with UNIQUE values",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT"),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="UK")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT"),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="UK")
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT"),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="UK")
            ]
        }
    ),
    SqlErrors.LOG_80_INCORRECT_FUNCTION: SqlErrorDetails(
        description="Incorrect function",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in the wrong aggregate function has been used (e.g. SUM instead of AVG). " \
            "The natural language query must be ambiguous to confuse the use of aggregate functions respect others (e.g. total can be SUM or COUNT).",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)            
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(2, state=True)            
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(3, state=True),
                constraints.query.HasSubQueryConstraint(state=True)            
            ]
        }
    ),
    SqlErrors.LOG_81_INCORRECT_COLUMN_AS_FUNCTION_PARAMETER: SqlErrorDetails(
        description="Incorrect column as function parameter",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in call function on the wrong column "
        "(e.g. EXTRACT(month FROM ts_start) instead of EXTRACT(month FROM ts_end)). The natural language query must be ambiguous to confuse the student in the choice " \
        "of columns that go into the functions.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True)            
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(2, state=True)            
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(3, state=True),
                constraints.query.HasSubQueryConstraint(state=True)            
            ]
        }
    ),
    SqlErrors.COM_83_UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE: SqlErrorDetails(
        description="Unnecessary DISTINCT in SELECT clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in SELECT which includes DISTINCT when it's not needed" \
        "(e.g. when we do select of a primary key that already return unique values). In solution there must be no DISTINCT.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(2, state=True)            
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(3, state=True),
                constraints.query.HasSubQueryConstraint(state=True)            
            ]
        }
    ),
    SqlErrors.COM_84_UNNECESSARY_JOIN: SqlErrorDetails(#puo essere migliorata?
        description="Unnecessary join",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in a table is joined even though only its PK is accessed "
        "(which we already have as FK). The solution in SELECT must have foreign keys to a table that are not used in joins.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(2, state=True)            
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(3, state=True),
                constraints.query.HasSubQueryConstraint(state=True)            
            ]
        }
    ),
    SqlErrors.COM_86_CORRELATION_NAMES_ARE_ALWAYS_IDENTICAL: SqlErrorDetails(
        description="Correlation names are always identical",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in two tables always " \
        "have the same data, because their PKs are equated and same alias as table. In the assignment create two table with " \
        "same PRIMARY KEY with same name (e.g. table 'tablename' with PK 'name_id' and table 'tablename_info' with PK 'name_id').",
        constraints={
            DifficultyLevel.EASY: [
                constraints.schema.HasSamePrimaryKeyConstraint(2), 
                constraints.query.HasWhereConstraint(2)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.schema.HasSamePrimaryKeyConstraint(2),
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasAggregationConstraint(2, state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.schema.HasSamePrimaryKeyConstraint(2), 
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(3, state=True),
                constraints.query.HasSubQueryConstraint(state=True)           
            ]
        }
    ),                         
    SqlErrors.COM_88_LIKE_WITHOUT_WILDCARDS: SqlErrorDetails(
        description="LIKE without wildcards",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using LIKE without any wildcards is the same wrong as using =. " \
        "The natural language query you must confuse the student by making him believe that the LIKE keyword is necessary. In the solution MUST NOT HAVE LIKE and WILDCARDS.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(type="NO WILDCARD")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(type="NO WILDCARD"),
                constraints.query.HasAggregationConstraint(2, state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(type="NO WILDCARD"),
                constraints.query.HasAggregationConstraint(3, state=True),
                constraints.query.HasSubQueryConstraint(state=True)           
            ]
        }
    ),
    SqlErrors.COM_89_UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY: SqlErrorDetails(
        description="Unnecessarily complicated SELECT in EXISTS subquery",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using more than one column in the SELECT clause " \
        "of an EXISTS subquery. In the solution must be EXISTS WITH only one column in SELECT and WITHOUT DISTINCT.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(type="EXIST"),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="DISTINCT")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type="EXIST"),
                constraints.query.HasSubQueryConstraint(2, state=True),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="DISTINCT")
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type="EXIST"),
                constraints.query.HasAggregationConstraint(3, state=True),
                constraints.query.HasSubQueryConstraint(3, state=True),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="DISTINCT")           
            ]
        }
    ),
    SqlErrors.COM_91_UNNECESSARY_AGGREGATE_FUNCTION: SqlErrorDetails(
        description="Unnecessary aggregate function",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using an aggregation function on a single value when it isn't necessary "
        "(e.g. (SELECT MAX(SAL) FROM EMP GROUP BY SAL) which is the same as (SELECT DISTINCT SAL FROM EMP)). In natural language query use term as 'maximum', 'minimum', " \
        "'count', 'average' ecc... that help to confuse the student but NOT use AGGREGATION.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=False),
                constraints.query.HasSubQueryConstraint(state=True)           
            ]
        }
    ),
    SqlErrors.COM_93_UNNECESSARY_ARGUMENT_OF_COUNT: SqlErrorDetails(
        description="Unnecessary argument of COUNT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using COUNT(column) instead of COUNT(*) when the column " \
        "cannot have NULL values. In solution must be the aggregation count with a star -> COUNT(*) .",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(1, state=True, type=["COUNT"])
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(1, state=True, type=["COUNT"])
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(1, state=True, type=["COUNT"]),
                constraints.query.HasSubQueryConstraint(state=True)           
            ]
        }
    ),
    SqlErrors.COM_95_GROUP_BY_WITH_SINGLETON_GROUPS: SqlErrorDetails(
        description="GROUP BY with singleton groups",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using GROUP BY when each group already consists of a single row " \
        "(e.g. GROUP BY id). The solution MUST HAVE GROUP BY but on NON UNIQUE columns",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=False),
                constraints.query.HasGroupByConstraint(1),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="UK")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=False),
                constraints.query.HasGroupByConstraint(2),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="UK")
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(state=False),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasGroupByConstraint(3),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=False, type="UK")
            ]
        }
    ),
    SqlErrors.COM_96_GROUP_BY_WITH_ONLY_A_SINGLE_GROUP: SqlErrorDetails(
        description="GROUP BY with only a single group",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in use grouping on " \
        "a column which contains the same value for all rows (e.g. SELECT job, COUNT(*) FROM t WHERE job = 'manager' GROUP BY job). " \
        "The solution must have in select ONLY aggregate functions.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasGroupByConstraint(state= False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(2, state=True),
                constraints.query.HasGroupByConstraint(state= False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasAggregationConstraint(3, state=True),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasGroupByConstraint(state= False)
            ]
        }
    ),
    SqlErrors.COM_97_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT: SqlErrorDetails(#controllare
        description="GROUP BY can be replaced with DISTINCT",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using GROUP BY when DISTINCT would suffice (e.g. SELECT DISTINCT col1, col2 FROM t instead of " \
        "SELECT col1, col2 FROM t GROUP BY col1, col2). In natural language query must create a query tahat can be solved with DISTINCT but the student can be confused to use GROUP BY.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasGroupByConstraint(state= False),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT")
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasGroupByConstraint(state= False),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT")
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasGroupByConstraint(state= False),
                constraints.query.HasDistinctOrUniqueKeyInSelectConstraint(state=True, type="DISTINCT")
            ]
        }
    ),
    SqlErrors.COM_98_UNION_CAN_BE_REPLACED_BY_OR: SqlErrorDetails(#controllare
        description="UNION can be replaced by OR",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in use UNION with two queries with: SAME tables in FROM, SAME column in SELECT and " \
        "mutually exclusive condition. The natural language query must have a request that can be solved with a single SELECT with OR in where condition or with UNION",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasUnionOrUnionAllConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasUnionOrUnionAllConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasUnionOrUnionAllConstraint(state=False)
            ]
        }
    ),
    SqlErrors.COM_99_UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE: SqlErrorDetails(
        description="Unnecessary column in ORDER BY clause",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in ordering the results by 2 column where one is functional depending on the other " \
        "(e.g. ORDER BY id_student, student_name). In natural language query MUST BE AMBIGUOUS on the order of the result table in ORDER BY clause, dont use the world 'Sort' or 'Order'.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasUnionOrUnionAllConstraint(state=False),
                constraints.query.HasOrderByConstraint(2)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasUnionOrUnionAllConstraint(state=False),
                constraints.query.HasOrderByConstraint(3)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasOrderByConstraint(4)
            ]
        }
    ),
    SqlErrors.COM_102_INEFFICIENT_UNION: SqlErrorDetails(
        description="Inefficient UNION",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using UNION instead of UNION ALL with two queries that are always disjoint or " \
        "don't return duplicates. In the natural language query you need to create a case where use of UNION ALL or UNION should be used depending on what request is made. In solution " \
        "if table in FROM are the same MUST USE UNION ALL, else if tables are different MUST USE UNION.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasUnionOrUnionAllConstraint(state=True)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasUnionOrUnionAllConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasUnionOrUnionAllConstraint(state=True)
            ]
        }
    ),
    SqlErrors.COM_104_CONDITION_ON_LEFT_TABLE_IN_LEFT_OUTER_JOIN: SqlErrorDetails(
        description="Condition on left table in LEFT OUTER JOIN",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using an ON condition on the LEFT table of an OUTER JOIN " \
        "instead of a condition on WHERE. The natural language query must create ambiguity about which table the condition applies to.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasJoinConstraint(left=True)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasJoinConstraint(left=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasJoinConstraint(2, left=True)
            ]
        }
    ),
    SqlErrors.COM_105_OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN: SqlErrorDetails(#controllare
        description="OUTER JOIN can be replaced by INNER JOIN",
        characteristics ="The exercise should naturally lead the student to make a mistake which consists in using a WHERE condition on the RIGHT table of an OUTER JOIN " \
        "instead of a condition on ON, making this equivalent to an INNER JOIN. In the solution must be INNER JOIN. The natural language query must create ambiguity about which JOIN " \
        "to use with words like 'right' and 'left'.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasJoinConstraint()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasJoinConstraint()
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasAggregationConstraint(state=True),
                constraints.query.HasJoinConstraint(2)
            ]
        }
    )
}
'''Mapping of SQL errors to their details.'''
