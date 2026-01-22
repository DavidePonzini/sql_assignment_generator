'''Descriptions and constraints for each supported SQL error.'''

# In error_details.py
from dataclasses import dataclass
from . import constraints
import random
from typing import Callable, Union
from .difficulty_level import DifficultyLevel
from sql_error_categorizer.sql_errors import SqlErrors
from .constraints.costraintType import WhereConstraintType

@dataclass
class SqlErrorDetails:
    '''Details about a specific SQL error, including description, characteristics, and constraints.'''
    description: str
    constraints: dict[DifficultyLevel, list[constraints.BaseConstraint]]
    exercise_characteristics: Union[str, Callable[[], str]] = ""
    dataset_characteristics: str = ""

ERROR_DETAILS_MAP = {
    SqlErrors.SYN_2_AMBIGUOUS_COLUMN: SqlErrorDetails(
        description="Ambiguous column",
        exercise_characteristics ="This exercise should require students to reference a column present in both table" \
        "In CREATE TABLE must share the SAME column name, excluding Primary Keys " \
        "(e.g. table 'person' with column 'name' and table 'doctor' with column 'name').",
        constraints={
            DifficultyLevel.EASY: [
                constraints.schema.HasSameColumnNameConstraint(min_tables=2),
                constraints.query.HasWhereConstraint(),
                constraints.query.RequireJoin(max_tables=1, min_tables=0),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.schema.HasSameColumnNameConstraint(min_tables=2),
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.schema.HasSameColumnNameConstraint(min_tables=3),
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SYN_4_UNDEFINED_COLUMN: SqlErrorDetails(
        description="Undefined column",
        exercise_characteristics = "This exercise should require students to reference a large number of columns in solution. " \
        "The solution must use the COLUMNS more COMPLEX and LONGER (e.g.'name_of_attribute'). ",
        constraints={
            DifficultyLevel.EASY: [
                constraints.schema.HasComplexColumnNameConstraint(min_complex_cols=2),
                constraints.query.HasWhereConstraint(),
                constraints.query.RequireJoin(max_tables=1, min_tables=0),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.NoHaving()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.schema.HasComplexColumnNameConstraint(min_complex_cols=4),
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.schema.HasComplexColumnNameConstraint(min_complex_cols=8),
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SYN_7_UNDEFINED_OBJECT: SqlErrorDetails(
        description="Undefined object",
        exercise_characteristics ="exercise should naturally tempts student to make a mistake which consist in reference to object that does not exist "
        "(e.g. SELECT * FROM player where table name is Players). In solution is necessary to make the table name more complex or longer.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(),
                constraints.query.RequireJoin(max_tables=1, min_tables=0),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.NoHaving()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SYN_9_MISSPELLINGS: SqlErrorDetails(
        description="Misspellings",
        exercise_characteristics ="The solution must use the COLUMNS more COMPLEX and LONGER (e.g.'name_of_attribute'). " \
        "The solution also MUST HAVE 2 or more similar columns",
        constraints={
            DifficultyLevel.EASY: [
                constraints.schema.HasComplexColumnNameConstraint(min_complex_cols=2),
                constraints.query.HasWhereConstraint(),
                constraints.query.RequireJoin(max_tables=1, min_tables=0),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.NoHaving()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.schema.HasComplexColumnNameConstraint(min_complex_cols=4),
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.schema.HasComplexColumnNameConstraint(min_complex_cols=8),
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_10_SYNONYMS: SqlErrorDetails(
        description="Synonyms",
        dataset_characteristics= "The identifier column name must NOT be <entity>_id; pick a plausible synonym " \
        "instead (e.g., <entity>_code, <entity>_key, <entity>_ref, <entity>_number,  etc)." \
        "Additionally, I  want  naming conventions NOT to be consistent across tables; different " \
        "tables must have different naming conventions for similar concepts: e.g. if Table1 uses "
        "(first_name, last_name), Table2 uses (name, surname)",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(),
                constraints.query.RequireJoin(max_tables=1, min_tables=0),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SYN_11_OMITTING_QUOTES_AROUND_CHARACTER_DATA: SqlErrorDetails(
        description="Omitting quotes around character data",
        exercise_characteristics ="iN THE exercise is mandatory use WHERE clause involving in many condition with " \
        "STRING variables (e.g. name = 'value').",
        dataset_characteristics="All the dataset column must have string attributes.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type = WhereConstraintType.STRING),
                constraints.query.RequireJoin(max_tables=1, min_tables=0),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type = WhereConstraintType.STRING),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type = WhereConstraintType.STRING),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SYN_12_FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE: SqlErrorDetails(
        description="Failure to specify column name twice",
        exercise_characteristics = "Solution query must have MULTIPLE CONDITION on the SAME COLUMN (e.g. p.film='Alien' OR p.film='Superman' this represent one column with MULTIPLE CONDITION). " \
            "Solution must not have IN format like 'position IN ('Manager', 'Supervisor')' but I want this format 'position ='Manager' OR position = 'Supervisor''" \
            "exercise should naturally tempts student to make a mistake that can cause 'miss column name' errors (e.g. WHERE city='Boston' OR 'Chicago').",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type = WhereConstraintType.MULTIPLE),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type = WhereConstraintType.MULTIPLE),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type = WhereConstraintType.MULTIPLE),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SYN_15_AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED: SqlErrorDetails(
        description="Grouping error: aggregate functions cannot be nested",
        exercise_characteristics ="Generate a query in natural language that seems to involve one AGGREGATION " \
        "inside another (e.g. 'the book that has the maximum number of sales' and in database doesn't store the sales count).",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.RequireAggregation(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation(2)
            ]
        }
    ),
    SqlErrors.SYN_19_USING_WHERE_TWICE: SqlErrorDetails(
        description="Using WHERE twice",
        exercise_characteristics ="exercise should naturally tempts student to make a mistake " \
        "that triggers use of multiple WHERE",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation(),
            ]
        }
    ),
    SqlErrors.SYN_21_COMPARISON_WITH_NULL: SqlErrorDetails(
        description="Comparison with NULL",
        exercise_characteristics ="In the exercise is mandatory use WHERE clause involving in " \
        "many condition with NULL value (e.g. column IS NULL) but only for non-key columns.",
        dataset_characteristics="Some non-key column in the dataset must have NULL values.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, 1, type=WhereConstraintType.NULL),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, 2, type=WhereConstraintType.NULL),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, 3, type=WhereConstraintType.NULL),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SYN_26_TOO_MANY_COLUMNS_IN_SUBQUERY: SqlErrorDetails(
        description="Too many COLUMNS in subquery",
        exercise_characteristics ="The solution in natural language must have comparison for each row must be compared with " \
        "a value from the same row or subset of rows (e.g. 'WHERE balance <comparison operator> (SELECT balance ... WHERE name = 'John')')",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.HasSubQueryConstraint(state=True, typeNested=False),
                constraints.query.NoHaving()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SYN_35_IS_WHERE_NOT_APPLICABLE: SqlErrorDetails(
        description="Use 'IS' where it's not applicable",
        exercise_characteristics ="The query in solution is mandatory that have WHERE conditions with use of '='",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SEM_39_AND_INSTEAD_OF_OR: SqlErrorDetails(
        description="AND instead of OR",
        exercise_characteristics ="Solution query must have OR MULTIPLE CONDITION on the SAME COLUMN "
        "(e.g. p.bornCity='Rome' OR p.bornCity='Genoa' this represent one column with MULTIPLE CONDITION). " \
        "It is mandatory use the parentesis to give precedence to separate condition. ",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type= WhereConstraintType.MULTIPLE),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(1, type= WhereConstraintType.MULTIPLE),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type= WhereConstraintType.MULTIPLE),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SEM_40_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION: SqlErrorDetails(
        description="Tautological or inconsistent expression",
        exercise_characteristics ="Solution query must have MULTIPLE CONDITION on the SAME COLUMN "
        "(e.g. p.age < 18 OR p.age >= 0 this represent one column with MULTIPLE CONDITION). ",
        dataset_characteristics="Table must have a CHECK.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.schema.HasCheckConstraint(1),
                constraints.query.HasWhereConstraint(1, type=WhereConstraintType.MULTIPLE),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.schema.HasCheckConstraint(2),
                constraints.query.HasWhereConstraint(1, type=WhereConstraintType.MULTIPLE),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.schema.HasCheckConstraint(3),
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.MULTIPLE),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SEM_41_DISTINCT_IN_SUM_OR_AVG: SqlErrorDetails(
        description="Use DISTINCT into SUM or AVG",
        exercise_characteristics = lambda: f''' The query in solution is mandatory that have DISTINCT and AGGREGATION of 
        type {random.choice(["AVG", "SUM"])} but MUST NOT insert DISTINCT inside the aggregation function. The solution must use
        DISTINCT outside the aggregation. The solution must not use any Key.
        ''',#mettere parola distinct nel testo ma il distinct non ci deve essere il group by si
        dataset_characteristics="The table must have non-key numeric attributes",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.RequireAggregation(1, allowed_functions=["SUM", "AVG"]),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.RequireAggregation(2, allowed_functions=["SUM", "AVG"]),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation(2, allowed_functions=["SUM", "AVG"]),
                constraints.query.HasDistinctConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SEM_42_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES: SqlErrorDetails(
        description="DISTINCT that might remove important duplicates",
        exercise_characteristics ="The solution must not have DISTINCT, UNIQUE KEY, AGGREGATION in SELECT clause and " \
        "must not have GROUP BY clause. It is necessary select attributes that can cause duplicates such as cities, names, etc." \
        "More specific attributes that can identify a record MUST NOT be selected (e.g. phone number, address, etc.).",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.NoAggregation(),
                constraints.query.NoGroupBy(),
                constraints.query.HasDistinctConstraint(state=False),
                constraints.query.HasUniqueKeyConstraint(state=False),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoAggregation(),
                constraints.query.NoGroupBy(),
                constraints.query.HasDistinctConstraint(state=False),
                constraints.query.HasUniqueKeyConstraint(state=False),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.NoAggregation(),
                constraints.query.NoGroupBy(),
                constraints.query.HasDistinctConstraint(state=False),
                constraints.query.HasUniqueKeyConstraint(state=False)
            ]
        }
    ),
    SqlErrors.SEM_43_WILDCARDS_WITHOUT_LIKE: SqlErrorDetails(
        description="Wildcards without LIKE",
        exercise_characteristics ="The query in solution is mandatory that have WHERE condition with use of WILDCARDS," \
        "in the WILDCARD insert whole words longer than 5 characters.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type=WhereConstraintType.WILDCARD),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.WILDCARD),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type=WhereConstraintType.WILDCARD),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SEM_44_INCORRECT_WILDCARD: SqlErrorDetails(
        description="Incorrect wildcard",
        exercise_characteristics =lambda: f'''Creates queries that must include 
        {random.choice(["+", "*", "()", "[]", "{}", "^", "%", "_"])} symbol in LIKE wildcard.''',
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type=WhereConstraintType.WILDCARD),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.WILDCARD),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type=WhereConstraintType.WILDCARD),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SEM_45_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL: SqlErrorDetails(
        description="Mixing a '> 0' with IS NOT NULL or empty string with NULL",
        dataset_characteristics= "Table must have some NULL values and numeric attributes",
        exercise_characteristics = lambda: f'''In the WHERE must have STRING and INTEGER condition that use 
        {random.choice([
            "Non-Nullable string", 
            "Nullable STRING",
            "INTEGER with comparison operator",
            "STRING Empty ('')"])
        }
        ''',
        #num >0 (num is not null), string = is null (string ='')
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NULL),
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NOT_NULL),
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.COMPARISON_OPERATORS),
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.EMPTY),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NULL),
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NOT_NULL),
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.EMPTY),
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.COMPARISON_OPERATORS),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NULL),
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NOT_NULL),
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.EMPTY),
                constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.COMPARISON_OPERATORS),
                #constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.SEM_46_NULL_IN_IN_ANY_ALL_SUBQUERY: SqlErrorDetails(
        description="NULL in IN/ANY/ALL subquery",
        exercise_characteristics =lambda: random.choice([
        "The query must select rows with a particular column higher/lower than at least one value in a subquery.", # col > ANY (subquery) | col < ANY (subquery)
        "The query must select the rows with the highest/lowest value of particular column.",   # col >= ALL (subquery) | col <= ALL (subquery)
        "The query must select rows where a particular column is equal to one value of a subquery." # col IN (subquery)
        ]),
        dataset_characteristics="Table must have some NULL values and numeric attributes",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),#type=WhereConstraintType.ANY_ALL_IN
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.NoHaving()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2), #type=WhereConstraintType.ANY_ALL_IN
                constraints.query.HasSubQueryConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3,), #type=WhereConstraintType.ANY_ALL_IN
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.SEM_49_MANY_DUPLICATES: SqlErrorDetails(
        description="Many duplicates",
        exercise_characteristics ="The solution must have DISTINCT in SELECT",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.NoHaving(),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.NoAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.NoAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.NoAggregation()
            ]
        }
    ),
    SqlErrors.LOG_52_OR_INSTEAD_OF_AND: SqlErrorDetails(
        description="OR instead of AND",
        exercise_characteristics ="Solution query must have more AND CONDITION (e.g. p.film='Eragon' AND p.type='Fantasy'). ",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation()
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_53_EXTRANEOUS_NOT_OPERATOR: SqlErrorDetails(
        description="Extraneous NOT operator",
        exercise_characteristics ="In the solution must have minimum one where without NOT in constraint",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_54_MISSING_NOT_OPERATOR: SqlErrorDetails(
        description="Missing NOT operator",
        exercise_characteristics ="In the solution must have more NOT to improve the learning of its use. ",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type=WhereConstraintType.NOT),
                constraints.query.HasWhereConstraint(1),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NOT),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NOT),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_55_SUBSTITUTING_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO: SqlErrorDetails(
        description="Substituting existence negation with <>",
        exercise_characteristics ="The query must select all Xs that are associated with all Ys (e.g. customers who " \
        "bought all products in category C, customer who bought all products that cost more than 50, etc.).",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, type=WhereConstraintType.NOT_EXIST),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=True)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NOT_EXIST),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NOT_EXIST),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),    
    SqlErrors.LOG_57_INCORRECT_COMPARISON_OPERATOR_OR_VALUE: SqlErrorDetails(
        description="Incorrect comparison operator or incorrect value compared",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.COMPARISON_OPERATORS),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.NoJoin()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.COMPARISON_OPERATORS),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type=WhereConstraintType.COMPARISON_OPERATORS),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_58_JOIN_ON_INCORRECT_TABLE: SqlErrorDetails(#join non rispetta max e min (58 59 62)
        description="Join on incorrect table",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.RequireJoin(min_tables=1, max_tables=1)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireJoin(2,3),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.RequireAggregation()
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireJoin(3,5),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_59_JOIN_WHEN_JOIN_NEEDS_TO_BE_OMITTED: SqlErrorDetails(
        description="Join when join needs to be omitted",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireJoin(1,1),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireJoin(2,3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireJoin(3,6),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_60_JOIN_ON_INCORRECT_COLUMN_MATCHES_POSSIBLE: SqlErrorDetails(
        description="Join on incorrect column (matches possible)",#difficili chiavi esterne composte
        dataset_characteristics ="In TABLE CREATION must have equal column with different meanings "
        "(e.g. users.name = products.name)",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireJoin(1),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireJoin(1),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireJoin(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_62_MISSING_JOIN: SqlErrorDetails(
        description="Missing join",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireJoin(1,1),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireJoin(2,3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireJoin(3,6),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_63_MPROPER_NESTING_OF_EXPRESSIONS: SqlErrorDetails(
        description="Improper nesting of expressions",
        exercise_characteristics ="Solution query must have multiple condition that must require NESTING "
        "(e.g. (condizione1 OR condizione2) AND condizione3 -> NESTING are the condition inside parentesis " \
        "which are MANDATORY).",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1, 1, type=WhereConstraintType.NESTED),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.NoHaving()
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NESTED),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NESTED),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.LOG_64_IMPROPER_NESTING_OF_SUBQUERIES: SqlErrorDetails(
        description="Improper nesting of subqueries",
        exercise_characteristics ="The exercise require use of sub-query NOT NESTED",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=True, typeNested=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasSubQueryConstraint(typeNested=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.HasSubQueryConstraint(typeNested=False),
                constraints.query.RequireAggregation()
            ]
        }
    ),
    SqlErrors.LOG_66_MISSING_EXPRESSION: SqlErrorDetails(
        description="Missing expression",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2,3),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3,5),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3,6),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_67_EXPRESSION_ON_INCORRECT_COLUMN: SqlErrorDetails(
        description="Expression on incorrect column",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_68_EXTRANEOUS_EXPRESSION: SqlErrorDetails(
        description="Extraneous expression",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_69_EXPRESSION_IN_INCORRECT_CLAUSE: SqlErrorDetails(
        description="Expression in incorrect clause",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.RequireHaving(1,1),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireHaving(1,3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireHaving(2,3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_70_EXTRANEOUS_COLUMN_IN_SELECT: SqlErrorDetails(#costraint per numero di colonne select
        description="Extraneous column in SELECT",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(0,0),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_71_MISSING_COLUMN_FROM_SELECT: SqlErrorDetails(#costraint per numero di colonne select
        description="Missing column from SELECT",
        exercise_characteristics ="The natural language query must be ambiguous and must require returning " \
        "many columns in SELECT statement, so that some columns may not be added by forgetfulness.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_72_MISSING_DISTINCT_FROM_SELECT: SqlErrorDetails(#dataset supporta duplicati e nella select selezionare i duplicati
        description="Missing DISTINCT from SELECT",
        dataset_characteristics="Create more duplicate data during insert (INSERT INTO ...)",
        exercise_characteristics ="The SELECT column must be attribute with duplicate data.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False)
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(),
                constraints.query.HasDistinctConstraint(state=True),
            ]
        }
    ),
    SqlErrors.LOG_73_MISSING_AS_FROM_SELECT: SqlErrorDetails(
        description="Missing AS from SELECT",
        exercise_characteristics ="The natural language query must ask to rename all column in SELECT.",#costraint per AS che ci sia
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_74_MISSING_COLUMN_FROM_ORDER_BY: SqlErrorDetails(#costraint colonne che facciamo per quelli sopra
        description="Missing column from ORDER BY clause",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasOrderByConstraint(1),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasOrderByConstraint(2),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasOrderByConstraint(3)
            ]
        }
    ),
    SqlErrors.LOG_75_INCORRECT_COLUMN_IN_ORDER_BY: SqlErrorDetails(#costraint colonne che facciamo per quelli sopra
        description="Incorrect column in ORDER BY clause",
        exercise_characteristics ="TThe natural language query must INDIRECTLY define the order in " \
        "which return the result table, that the student will insert into ORDER BY.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasOrderByConstraint(1),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasOrderByConstraint(2),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasOrderByConstraint(3)
            ]
        }
    ),
    SqlErrors.LOG_76_EXTRANEOUS_ORDER_BY_CLAUSE: SqlErrorDetails(
        description="Extraneous ORDER BY clause",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.HasOrderByConstraint(state=False),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasOrderByConstraint(state=False),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasOrderByConstraint(state=False)
            ]
        }
    ),     
    SqlErrors.LOG_77_INCORRECT_ORDERING_OF_ROWS: SqlErrorDetails(#opzione del ASC, DSC
        description="Incorrect ordering of rows",
        exercise_characteristics ="The natural language query must be ambiguous, " \
        "not making the order of the columns clear and simple.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasOrderByConstraint(),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(),
                constraints.query.HasOrderByConstraint(2),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasOrderByConstraint(3)
            ]
        }
    ),
    SqlErrors.LOG_78_DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE: SqlErrorDetails(
        description="DISTINCT as function parameter where not applicable",
        dataset_characteristics= "Create more duplicate data during insert (INSERT INTO ...)",
        exercise_characteristics ="The solution query must have following structure:" \
        '''SELECT DISTINCT c
            FROM ( SELECT col_1 [, col2 [,col_n]], COUNT(*) c
                    FROM table
                    GROUP BY col_1 [, col_2 [, col_n]] 
            )''',
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(1),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.RequireAggregation(allowed_functions=["COUNT"]),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=True),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(allowed_functions=["COUNT"]),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=True),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(allowed_functions=["COUNT"]),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasDistinctConstraint(state=True)
            ]
        }
    ),
    SqlErrors.LOG_79_MISSING_DISTINCT_FROM_FUNCTION_PARAMETER: SqlErrorDetails(
        description="Missing DISTINCT from function parameter",
        exercise_characteristics = "The exercise must NOT have PRIMARY KEY inside COUNT, "
        "and must have DISTINCT inside COUNT",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.RequireAggregation(allowed_functions=["COUNT"]),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(allowed_functions=["COUNT"]),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.HasUniqueKeyConstraint(state=False),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(allowed_functions=["COUNT"]),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.HasUniqueKeyConstraint(state=False)
            ]
        }
    ),
    SqlErrors.LOG_80_INCORRECT_FUNCTION: SqlErrorDetails(
        description="Incorrect function",
        exercise_characteristics ="The natural language query must be ambiguous to confuse the use of " \
        "aggregate functions respect others (e.g. total can be SUM or COUNT).",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False),           
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(3),
                constraints.query.HasSubQueryConstraint(state=True)            
            ]
        }
    ),
    SqlErrors.LOG_81_INCORRECT_COLUMN_AS_FUNCTION_PARAMETER: SqlErrorDetails(
        description="Incorrect column as function parameter",
        exercise_characteristics ="The natural language query must be ambiguous to confuse the student in the choice " \
        "of columns that go into the functions.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),           
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False),            
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(3),
                constraints.query.HasSubQueryConstraint(state=True)            
            ]
        }
    ),
    SqlErrors.COM_83_UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE: SqlErrorDetails(
        description="Unnecessary DISTINCT in SELECT clause",
        exercise_characteristics ="In solution there must be no DISTINCT.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasDistinctConstraint(state=False),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(2),
                constraints.query.HasDistinctConstraint(state=False),
                constraints.query.HasSubQueryConstraint(state=False),           
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasDistinctConstraint(state=False),            
            ]
        }
    ),
    SqlErrors.COM_84_UNNECESSARY_JOIN: SqlErrorDetails(
        description="Unnecessary join",
        dataset_characteristics ="In TABLE CREATION must be FOREIGN KEY relationship between tables ",
        exercise_characteristics="In the solution query must be selected ONLY FOREIGN KEY column for at least one table in select.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False),
                constraints.query.HasSubQueryConstraint(state=False),        
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(3),
                constraints.query.HasSubQueryConstraint(state=True)            
            ]
        }
    ),
    SqlErrors.COM_86_CORRELATION_NAMES_ARE_ALWAYS_IDENTICAL: SqlErrorDetails(
        description="Correlation names are always identical",
        dataset_characteristics="In the assignment create two table with same PRIMARY KEY with same name "
        "(e.g. table 'tablename' with PK 'name_id' and table 'tablename_info' with PK 'name_id').",
        constraints={
            DifficultyLevel.EASY: [
                constraints.schema.HasSamePrimaryKeyConstraint(2), 
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.schema.HasSamePrimaryKeyConstraint(2),
                constraints.query.HasWhereConstraint(3),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.schema.HasSamePrimaryKeyConstraint(2), 
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(3),
                constraints.query.HasSubQueryConstraint(state=True)           
            ]
        }
    ),                         
    SqlErrors.COM_88_LIKE_WITHOUT_WILDCARDS: SqlErrorDetails(
        description="LIKE without wildcards",
        exercise_characteristics ="The natural language query you must confuse the student by making him " \
        "believe that the LIKE keyword is necessary. In the solution MUST NOT HAVE LIKE and WILDCARDS.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(type=WhereConstraintType.NO_WILDCARD),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(type=WhereConstraintType.NO_WILDCARD),
                constraints.query.RequireAggregation(2),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(type=WhereConstraintType.NO_WILDCARD),
                constraints.query.RequireAggregation(3),
                constraints.query.HasSubQueryConstraint(state=True)           
            ]
        }
    ),
    SqlErrors.COM_89_UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY: SqlErrorDetails(
        description="Unnecessarily complicated SELECT in EXISTS subquery",
        exercise_characteristics ="In the solution must be EXISTS WITH only one column in SELECT and WITHOUT DISTINCT.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(type=WhereConstraintType.EXIST),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.HasDistinctConstraint(state=False),
                constraints.query.NoHaving(),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2, type=WhereConstraintType.EXIST),
                constraints.query.HasSubQueryConstraint(2, state=True),
                constraints.query.HasDistinctConstraint(state=False)
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(3, type=WhereConstraintType.EXIST),
                constraints.query.RequireAggregation(3),
                constraints.query.HasSubQueryConstraint(3, state=True),
                constraints.query.HasDistinctConstraint(state=False)           
            ]
        }
    ),
    SqlErrors.COM_91_UNNECESSARY_AGGREGATE_FUNCTION: SqlErrorDetails(
        description="Unnecessary aggregate function",
        exercise_characteristics ="In natural language query use term as 'maximum', 'minimum', " \
        "'count', 'average' ecc... that help to confuse the student but NOT use AGGREGATION.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoAggregation(),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoAggregation(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.NoAggregation(),
                constraints.query.HasSubQueryConstraint(state=True)           
            ]
        }
    ),
    SqlErrors.COM_93_UNNECESSARY_ARGUMENT_OF_COUNT: SqlErrorDetails(
        description="Unnecessary argument of COUNT",
        exercise_characteristics ="In solution must be the aggregation count with a star -> COUNT(*) .",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(1),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(1),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(1),
                constraints.query.HasSubQueryConstraint(state=True)           
            ]
        }
    ),
    SqlErrors.COM_95_GROUP_BY_WITH_SINGLETON_GROUPS: SqlErrorDetails(
        description="GROUP BY with singleton groups",
        exercise_characteristics ="The solution MUST HAVE GROUP BY but on NON UNIQUE columns",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoAggregation(),
                constraints.query.RequireGroupBy(1),
                constraints.query.HasDistinctConstraint(state=False),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoAggregation(),
                constraints.query.RequireGroupBy(2),
                constraints.query.HasDistinctConstraint(state=False),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.NoAggregation(),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireGroupBy(3),
                constraints.query.HasDistinctConstraint(state=False)
            ]
        }
    ),
    SqlErrors.COM_96_GROUP_BY_WITH_ONLY_A_SINGLE_GROUP: SqlErrorDetails(
        description="GROUP BY with only a single group",
        exercise_characteristics ="The solution must have in select ONLY aggregate functions.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.NoGroupBy(),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(2),
                constraints.query.NoGroupBy(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.RequireAggregation(3),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.NoGroupBy()
            ]
        }
    ),
    SqlErrors.COM_97_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT: SqlErrorDetails(#controllare
        description="GROUP BY can be replaced with DISTINCT",
        exercise_characteristics ="In natural language query must create a query tahat can be solved with " \
        "DISTINCT but the student can be confused to use GROUP BY.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoGroupBy(),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.NoGroupBy(),
                constraints.query.HasDistinctConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.NoGroupBy(),
                constraints.query.HasDistinctConstraint(state=True)
            ]
        }
    ),
    SqlErrors.COM_98_UNION_CAN_BE_REPLACED_BY_OR: SqlErrorDetails(#controllare
        description="UNION can be replaced by OR",
        exercise_characteristics ="The natural language query must have a request that can be solved with a " \
        "single SELECT with OR in where condition or with UNION",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasUnionOrUnionAllConstraint(state=False),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasUnionOrUnionAllConstraint(state=False),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation(),
                constraints.query.HasUnionOrUnionAllConstraint(state=False)
            ]
        }
    ),
    SqlErrors.COM_99_UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE: SqlErrorDetails(
        description="Unnecessary column in ORDER BY clause",
        exercise_characteristics ="In natural language query MUST BE AMBIGUOUS on the order of " \
        "the result table in ORDER BY clause, dont use the world 'Sort' or 'Order'.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasUnionOrUnionAllConstraint(state=False),
                constraints.query.HasOrderByConstraint(2),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasUnionOrUnionAllConstraint(state=False),
                constraints.query.HasOrderByConstraint(3),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation(),
                constraints.query.HasOrderByConstraint(4)
            ]
        }
    ),
    SqlErrors.COM_102_INEFFICIENT_UNION: SqlErrorDetails(
        description="Inefficient UNION",
        exercise_characteristics ="In the natural language query you need to create a case where use of " \
        "UNION ALL or UNION should be used depending on what request is made. In solution " \
        "if table in FROM are the same MUST USE UNION ALL, else if tables are different MUST USE UNION.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.HasUnionOrUnionAllConstraint(state=True),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.HasUnionOrUnionAllConstraint(state=True),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation(),
                constraints.query.HasUnionOrUnionAllConstraint(state=True)
            ]
        }
    ),
    SqlErrors.COM_104_CONDITION_ON_LEFT_TABLE_IN_LEFT_OUTER_JOIN: SqlErrorDetails(
        description="Condition on left table in LEFT OUTER JOIN",
        exercise_characteristics ="The natural language query must create ambiguity about which table " \
        "the condition applies to.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireJoin(left=True),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.RequireJoin(left=True),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation(),
                constraints.query.RequireJoin(2, left=True)
            ]
        }
    ),
    SqlErrors.COM_105_OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN: SqlErrorDetails(#controllare
        description="OUTER JOIN can be replaced by INNER JOIN",
        exercise_characteristics ="he natural language query must create ambiguity about which JOIN " \
        "to use with words like 'right' and 'left'.",
        constraints={
            DifficultyLevel.EASY: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireJoin(),
                constraints.query.NoHaving(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.MEDIUM: [
                constraints.query.HasWhereConstraint(2),
                constraints.query.RequireAggregation(),
                constraints.query.RequireJoin(),
                constraints.query.HasSubQueryConstraint(state=False),
            ],
            DifficultyLevel.HARD: [
                constraints.query.HasWhereConstraint(4),
                constraints.query.HasSubQueryConstraint(state=True),
                constraints.query.RequireAggregation(),
                constraints.query.RequireJoin(2)
            ]
        }
    )
}
'''Mapping of SQL errors to their details.'''
