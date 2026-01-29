'''Descriptions and constraints for each supported SQL error.'''

# In error_details.py
from dataclasses import dataclass

from .error_requirements import SqlErrorRequirements
from . import constraints
import random
from typing import Callable, Union
from .difficulty_level import DifficultyLevel
from sql_error_taxonomy import SqlErrors
from .constraints.costraintType import WhereConstraintType
from .error_requirements import *






#     SqlErrors.SYN_2_AMBIGUOUS_COLUMN: SqlErrorRequirements(
#         description="Ambiguous column",
#         exercise_extra_details ="This exercise should require students to reference a column present in both table" \
#         "In CREATE TABLE must share the SAME column name, excluding Primary Keys " \
#         "(e.g. table 'person' with column 'name' and table 'doctor' with column 'name').",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.schema.SameColumnNames(min_tables=2),
#                 constraints.query.HasWhereConstraint(),
#                 constraints.query.Join(max_=1, min_=0),
#                 constraints.query.NoSubquery(),
#                 constraints.query.NoHaving(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.schema.SameColumnNames(min_tables=2),
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.schema.SameColumnNames(min_tables=3),
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SYN_4_UNDEFINED_COLUMN: SqlErrorRequirements(
#         description="Undefined column",
#         exercise_extra_details = "This exercise should require students to reference a large number of columns in solution. " \
#         "The solution must use the COLUMNS more COMPLEX and LONGER (e.g.'name_of_attribute'). ",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.schema.ComplexColumnName(min_columns=2),
#                 constraints.query.HasWhereConstraint(),
#                 constraints.query.Join(max_=1, min_=0),
#                 constraints.query.NoSubquery(),
#                 constraints.query.NoHaving()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.schema.ComplexColumnName(min_columns=4),
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.schema.ComplexColumnName(min_columns=8),
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.RequireSubqueries(state=True),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SYN_7_UNDEFINED_OBJECT: SqlErrorRequirements(
#         description="Undefined object",
#         exercise_extra_details ="exercise should naturally tempts student to make a mistake which consist in reference to object that does not exist "
#         "(e.g. SELECT * FROM player where table name is Players). In solution is necessary to make the table name more complex or longer.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(),
#                 constraints.query.Join(max_=1, min_=0),
#                 constraints.query.NoSubquery(),
#                 constraints.query.NoHaving()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SYN_9_MISSPELLINGS: SqlErrorRequirements(
#         description="Misspellings",
#         exercise_extra_details ="The solution must use the COLUMNS more COMPLEX and LONGER (e.g.'name_of_attribute'). " \
#         "The solution also MUST HAVE 2 or more similar columns",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.schema.ComplexColumnName(min_columns=2),
#                 constraints.query.HasWhereConstraint(),
#                 constraints.query.Join(max_=1, min_=0),
#                 constraints.query.NoSubquery(),
#                 constraints.query.NoHaving()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.schema.ComplexColumnName(min_columns=4),
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.schema.ComplexColumnName(min_columns=8),
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.SYN_10_SYNONYMS: SqlErrorRequirements(
#         description="Synonyms",
#         dataset_extra_details= "The identifier column name must NOT be <entity>_id; pick a plausible synonym " \
#         "instead (e.g., <entity>_code, <entity>_key, <entity>_ref, <entity>_number,  etc)." \
#         "Additionally, I  want  naming conventions NOT to be consistent across tables; different " \
#         "tables must have different naming conventions for similar concepts: e.g. if Table1 uses "
#         "(first_name, last_name), Table2 uses (name, surname)",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(),
#                 constraints.query.Join(max_=1, min_=0),
#                 constraints.query.NoSubquery(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SYN_11_OMITTING_QUOTES_AROUND_CHARACTER_DATA: SqlErrorRequirements(
#         description="Omitting quotes around character data",
#         exercise_extra_details ="iN THE exercise is mandatory use WHERE clause involving in many condition with " \
#         "STRING variables (e.g. name = 'value').",
#         dataset_extra_details="All the dataset column must have string attributes.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1, type = WhereConstraintType.STRING),
#                 constraints.query.Join(max_=1, min_=0),
#                 constraints.query.NoSubquery(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2, type = WhereConstraintType.STRING),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3, type = WhereConstraintType.STRING),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SYN_12_FAILURE_TO_SPECIFY_COLUMN_NAME_TWICE: SqlErrorRequirements(
#         description="Failure to specify column name twice",
#         exercise_extra_details = "Solution query must have MULTIPLE CONDITION on the SAME COLUMN (e.g. p.film='Alien' OR p.film='Superman' this represent one column with MULTIPLE CONDITION). " \
#             "Solution must not have IN format like 'position IN ('Manager', 'Supervisor')' but I want this format 'position ='Manager' OR position = 'Supervisor''" \
#             "exercise should naturally tempts student to make a mistake that can cause 'miss column name' errors (e.g. WHERE city='Boston' OR 'Chicago').",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1, type = WhereConstraintType.MULTIPLE),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2, type = WhereConstraintType.MULTIPLE),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(2, type = WhereConstraintType.MULTIPLE),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SYN_15_AGGREGATE_FUNCTIONS_CANNOT_BE_NESTED: SqlErrorRequirements(
#         description="Grouping error: aggregate functions cannot be nested",
#         exercise_extra_details ="Generate a query in natural language that seems to involve one AGGREGATION " \
#         "inside another (e.g. 'the book that has the maximum number of sales' and in database doesn't store the sales count).",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation(2)
#             ]
#         }
#     ),
#     SqlErrors.SYN_19_USING_WHERE_TWICE: SqlErrorRequirements(
#         description="Using WHERE twice",
#         exercise_extra_details ="exercise should naturally tempts student to make a mistake " \
#         "that triggers use of multiple WHERE",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation(),
#             ]
#         }
#     ),
#     SqlErrors.SYN_21_COMPARISON_WITH_NULL: SqlErrorRequirements(
#         description="Comparison with NULL",
#         exercise_extra_details ="In the exercise is mandatory use WHERE clause involving in " \
#         "many condition with NULL value (e.g. column IS NULL) but only for non-key columns.",
#         dataset_extra_details="Some non-key column in the dataset must have NULL values.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1, 1, type=WhereConstraintType.NULL),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2, 2, type=WhereConstraintType.NULL),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3, 3, type=WhereConstraintType.NULL),
#                 constraints.query.NoHaving(),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SYN_26_TOO_MANY_COLUMNS_IN_SUBQUERY: SqlErrorRequirements(
#         description="Too many COLUMNS in subquery",
#         exercise_extra_details ="The solution in natural language must have comparison for each row must be compared with " \
#         "a value from the same row or subset of rows (e.g. 'WHERE balance <comparison operator> (SELECT balance ... WHERE name = 'John')')",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.UnnestedSubqueries(),
#                 constraints.query.NoHaving()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.RequireSubqueries()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(2),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.SYN_35_IS_WHERE_NOT_APPLICABLE: SqlErrorRequirements(
#         description="Use 'IS' where it's not applicable",
#         exercise_extra_details ="The query in solution is mandatory that have WHERE conditions with use of '='",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SEM_39_AND_INSTEAD_OF_OR: SqlErrorRequirements(
#         description="AND instead of OR",
#         exercise_extra_details ="Solution query must have OR MULTIPLE CONDITION on the SAME COLUMN "
#         "(e.g. p.bornCity='Rome' OR p.bornCity='Genoa' this represent one column with MULTIPLE CONDITION). " \
#         "It is mandatory use the parentesis to give precedence to separate condition. ",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1, type= WhereConstraintType.MULTIPLE),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(1, type= WhereConstraintType.MULTIPLE),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(2, type= WhereConstraintType.MULTIPLE),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SEM_40_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION: SqlErrorRequirements(
#         description="Tautological or inconsistent expression",
#         exercise_extra_details ="Solution query must have MULTIPLE CONDITION on the SAME COLUMN "
#         "(e.g. p.age < 18 OR p.age >= 0 this represent one column with MULTIPLE CONDITION). ",
#         dataset_extra_details="Table must have a CHECK.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.schema.MinChecks(1),
#                 constraints.query.HasWhereConstraint(1, type=WhereConstraintType.MULTIPLE),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.schema.MinChecks(2),
#                 constraints.query.HasWhereConstraint(1, type=WhereConstraintType.MULTIPLE),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.schema.MinChecks(3),
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.MULTIPLE),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SEM_41_DISTINCT_IN_SUM_OR_AVG: SqlErrorRequirements(
#         description="Use DISTINCT into SUM or AVG",
#         exercise_extra_details = lambda: f''' The query in solution is mandatory that have AGGREGATION of 
#         type {random.choice(["AVG", "SUM"])}. In the natural language query must have explaination word 'distinct'
#         but NOT DISTINCT clausole in query.''',#mettere parola distinct nel testo ma il distinct non ci deve essere, il group by si
#         dataset_extra_details="The table must have non-key numeric attributes",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.Aggregation(1, allowed_functions=["SUM", "AVG"]),
#                 constraints.query.NoDistinct(),
#                 constraints.query.NoSubquery(),
#                 constraints.query.GroupBy(),
#                 constraints.query.NoHaving()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.Aggregation(2, allowed_functions=["SUM", "AVG"]),
#                 constraints.query.NoDistinct(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation(2, allowed_functions=["SUM", "AVG"]),
#                 constraints.query.Distinct()
#             ]
#         }
#     ),
#     SqlErrors.SEM_42_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES: SqlErrorRequirements(
#         description="DISTINCT that might remove important duplicates",
#         exercise_extra_details ="The solution must not have DISTINCT, UNIQUE KEY, AGGREGATION in SELECT clause and " \
#         "must not have GROUP BY clause. It is necessary select attributes that can cause duplicates such as cities, names, etc." \
#         "More specific attributes that can identify a record MUST NOT be selected (e.g. phone number, address, etc.).",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.NoAggregation(),
#                 constraints.query.NoGroupBy(),
#                 constraints.query.NoDistinct(),
#                 constraints.query.HasUniqueKeyConstraint(state=False),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoAggregation(),
#                 constraints.query.NoGroupBy(),
#                 constraints.query.NoDistinct(),
#                 constraints.query.HasUniqueKeyConstraint(state=False),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.NoAggregation(),
#                 constraints.query.NoGroupBy(),
#                 constraints.query.NoDistinct(),
#                 constraints.query.HasUniqueKeyConstraint(state=False)
#             ]
#         }
#     ),
#     SqlErrors.SEM_43_WILDCARDS_WITHOUT_LIKE: SqlErrorRequirements(
#         description="Wildcards without LIKE",
#         exercise_extra_details ="The query in solution is mandatory that have WHERE condition with use of WILDCARDS," \
#         "in the WILDCARD insert whole words longer than 5 characters.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1, type=WhereConstraintType.WILDCARD),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.WILDCARD),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3, type=WhereConstraintType.WILDCARD),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SEM_44_INCORRECT_WILDCARD: SqlErrorRequirements(
#         description="Incorrect wildcard",
#         exercise_extra_details =lambda: f'''Creates queries that must include 
#         {random.choice(["+", "*", "()", "[]", "{}", "^", "%", "_"])} symbol in LIKE wildcard.''',
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1, type=WhereConstraintType.WILDCARD),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.WILDCARD),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3, type=WhereConstraintType.WILDCARD),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SEM_45_MIXING_A_GREATER_THAN_0_WITH_IS_NOT_NULL: SqlErrorRequirements(
#         description="Mixing a '> 0' with IS NOT NULL or empty string with NULL",
#         dataset_extra_details= "Table must have some NULL, Non-NULL, empty and NUMERIC attributes",
#         exercise_extra_details = lambda: f'''In the WHERE must have minimun one  
#         {random.choice([
#             "STRING value with NOT NULL condition (IS NOT NULL)", 
#             "STRING value with NULL condition (IS NULL)",
#             "INTEGER value with comparison operator condition (>, <, =, <=, >=...)",
#             "STRING value with Empty condition (column = '')"])
#         }
#         ''',
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NULL),
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NOT_NULL),
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.COMPARISON_OPERATORS),
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.EMPTY),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NULL),
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NOT_NULL),
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.EMPTY),
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.COMPARISON_OPERATORS),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NULL),
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.NOT_NULL),
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.EMPTY),
#                 constraints.query.HasWhereConstraint(0, 1, type=WhereConstraintType.COMPARISON_OPERATORS),
#                 #constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.SEM_46_NULL_IN_IN_ANY_ALL_SUBQUERY: SqlErrorRequirements(
#         description="NULL in IN/ANY/ALL subquery",
#         exercise_extra_details =lambda: random.choice([
#         "The query must select rows with a particular column higher/lower than at least one value in a subquery.", # col > ANY (subquery) | col < ANY (subquery)
#         "The query must select the rows with the highest/lowest value of particular column.",   # col >= ALL (subquery) | col <= ALL (subquery)
#         "The query must select rows where a particular column is equal to one value of a subquery." # col IN (subquery)
#         ]),
#         dataset_extra_details="Table must have some NULL values and numeric attributes",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1),#type=WhereConstraintType.ANY_ALL_IN
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.NoHaving()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2), #type=WhereConstraintType.ANY_ALL_IN
#                 constraints.query.RequireSubqueries()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3,), #type=WhereConstraintType.ANY_ALL_IN
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.SEM_49_MANY_DUPLICATES: SqlErrorRequirements(
#         description="Many duplicates",
#         exercise_extra_details ="The solution must have DISTINCT in SELECT",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.NoHaving(),
#                 constraints.query.Distinct(),
#                 constraints.query.NoAggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Distinct(),
#                 constraints.query.NoAggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Distinct(),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.NoAggregation()
#             ]
#         }
#     ),
#     SqlErrors.LOG_52_OR_INSTEAD_OF_AND: SqlErrorRequirements(
#         description="OR instead of AND",
#         exercise_extra_details ="Solution query must have more AND CONDITION (e.g. p.film='Eragon' AND p.type='Fantasy'). ",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2)
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_53_EXTRANEOUS_NOT_OPERATOR: SqlErrorRequirements(
#         description="Extraneous NOT operator",
#         exercise_extra_details ="In the solution must have minimum one where without NOT in constraint",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_54_MISSING_NOT_OPERATOR: SqlErrorRequirements(
#         description="Missing NOT operator",
#         exercise_extra_details ="In the solution must have more NOT to improve the learning of its use. ",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1, type=WhereConstraintType.NOT),
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NOT),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NOT),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_55_SUBSTITUTING_EXISTENCE_NEGATION_WITH_NOT_EQUAL_TO: SqlErrorRequirements(
#         description="Substituting existence negation with <>",
#         exercise_extra_details ="The query must select all Xs that are associated with all Ys (e.g. customers who " \
#         "bought all products in category C, customer who bought all products that cost more than 50, etc.).",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1, type=WhereConstraintType.NOT_EXIST),
#                 constraints.query.NoHaving(),
#                 constraints.query.RequireSubqueries()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NOT_EXIST),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NOT_EXIST),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),    
#     SqlErrors.LOG_57_INCORRECT_COMPARISON_OPERATOR_OR_VALUE: SqlErrorRequirements(
#         description="Incorrect comparison operator or incorrect value compared",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.COMPARISON_OPERATORS),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#                 constraints.query.NoJoin()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.COMPARISON_OPERATORS),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3, type=WhereConstraintType.COMPARISON_OPERATORS),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_58_JOIN_ON_INCORRECT_TABLE: SqlErrorRequirements(
#         description="Join on incorrect table",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#                 constraints.query.Join(min_=1, max_=1)
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Join(2,3),
#                 constraints.query.NoSubquery(),
#                 constraints.query.Aggregation()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Join(3,5),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_59_JOIN_WHEN_JOIN_NEEDS_TO_BE_OMITTED: SqlErrorRequirements(
#         description="Join when join needs to be omitted",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Join(1,1),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Join(2,3),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Join(3,6),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_60_JOIN_ON_INCORRECT_COLUMN_MATCHES_POSSIBLE: SqlErrorRequirements(
#         description="Join on incorrect column (matches possible)",
#         dataset_extra_details ="In TABLE CREATION must be composite FOREIGN KEY",
#         exercise_extra_details="Solution MUST USE composite FOREIGN KEY in join "
#         "(e.g. column1 a JOIN column2 b ON (a.col1= b.col1) AND (a.col2 = b.col2))",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Join(1),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Join(1),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Join(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_62_MISSING_JOIN: SqlErrorRequirements(
#         description="Missing join",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Join(1,1),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Join(2,3),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Join(3,6),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_63_MPROPER_NESTING_OF_EXPRESSIONS: SqlErrorRequirements(
#         description="Improper nesting of expressions",
#         exercise_extra_details ="Solution query must have multiple condition that must require NESTING "
#         "(e.g. (condizione1 OR condizione2) AND condizione3 -> NESTING are the condition inside parentesis " \
#         "which are MANDATORY).",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1, 1, type=WhereConstraintType.NESTED),
#                 constraints.query.NoSubquery(),
#                 constraints.query.NoHaving()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NESTED),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.NESTED),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.LOG_64_IMPROPER_NESTING_OF_SUBQUERIES: SqlErrorRequirements(
#         description="Improper nesting of subqueries",
#         exercise_extra_details ="The exercise require use of sub-query NOT NESTED",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.NoHaving(),
#                 constraints.query.UnnestedSubqueries(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.UnnestedSubqueries()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.UnnestedSubqueries(),
#                 constraints.query.Aggregation()
#             ]
#         }
#     ),
#     SqlErrors.LOG_66_MISSING_EXPRESSION: SqlErrorRequirements(
#         description="Missing expression",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2,3),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3,5),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3,6),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_67_EXPRESSION_ON_INCORRECT_COLUMN: SqlErrorRequirements(
#         description="Expression on incorrect column",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_68_EXTRANEOUS_EXPRESSION: SqlErrorRequirements(
#         description="Extraneous expression",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_69_EXPRESSION_IN_INCORRECT_CLAUSE: SqlErrorRequirements(
#         description="Expression in incorrect clause",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.Having(1,1),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Having(1,3),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Having(2,3),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_70_EXTRANEOUS_COLUMN_IN_SELECT: SqlErrorRequirements(
#         description="Extraneous column in SELECT",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(0,0),
#                 constraints.query.SelectedColumns(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.SelectedColumns(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.SelectedColumns(4),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_71_MISSING_COLUMN_FROM_SELECT: SqlErrorRequirements(
#         description="Missing column from SELECT",
#         exercise_extra_details ="The natural language query must be ambiguous and must require returning " \
#         "many columns in SELECT statement, so that some columns may not be added by forgetfulness.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.SelectedColumns(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.SelectedColumns(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.SelectedColumns(4),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_72_MISSING_DISTINCT_FROM_SELECT: SqlErrorRequirements(#dataset supporta duplicati e nella select selezionare i duplicati
#         description="Missing DISTINCT from SELECT",
#         dataset_extra_details="Create more duplicate information during insert data (INSERT INTO ...)",
#         exercise_extra_details ="The SELECT column must be attribute with duplicate data.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Distinct(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery()
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.Distinct(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Distinct(),
#             ]
#         }
#     ),
#     SqlErrors.LOG_73_MISSING_AS_FROM_SELECT: SqlErrorRequirements(
#         description="Missing AS from SELECT",
#         exercise_extra_details ="The natural language query must ask to rename all column in SELECT.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Alias(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Alias(),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Alias(),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries()
#             ]
#         }
#     ),
#     SqlErrors.LOG_74_MISSING_COLUMN_FROM_ORDER_BY: SqlErrorRequirements(
#         description="Missing column from ORDER BY clause",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.OrderBy(1),
#                 constraints.query.SelectedColumns(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.SelectedColumns(3),
#                 constraints.query.OrderBy(2),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(),
#                 constraints.query.SelectedColumns(4),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.OrderBy(3)
#             ]
#         }
#     ),
#     SqlErrors.LOG_75_INCORRECT_COLUMN_IN_ORDER_BY: SqlErrorRequirements(
#         description="Incorrect column in ORDER BY clause",
#         exercise_extra_details ="The natural language query must INDIRECTLY define the order in " \
#         "which return the result table, that the student will insert into ORDER BY.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.OrderBy(1),
#                 constraints.query.SelectedColumns(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.SelectedColumns(3),
#                 constraints.query.OrderBy(2),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(),
#                 constraints.query.SelectedColumns(4),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.OrderBy(3)
#             ]
#         }
#     ),
#     SqlErrors.LOG_76_EXTRANEOUS_ORDER_BY_CLAUSE: SqlErrorRequirements(
#         description="Extraneous ORDER BY clause",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.OrderBy(state=False),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.OrderBy(state=False),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.OrderBy(state=False)
#             ]
#         }
#     ),     
#     SqlErrors.LOG_77_INCORRECT_ORDERING_OF_ROWS: SqlErrorRequirements(
#         description="Incorrect ordering of rows",
#         exercise_extra_details ="The natural language query ABSOLUTELY MUST NOT HAVE 'in descending order'.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.OrderBy(is_desc=True),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(),
#                 constraints.query.OrderBy(2, is_desc=True),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.OrderBy(3, is_desc=True)
#             ]
#         }
#     ),
#     SqlErrors.LOG_78_DISTINCT_AS_FUNCTION_PARAMETER_WHERE_NOT_APPLICABLE: SqlErrorRequirements(
#         description="DISTINCT as function parameter where not applicable",
#         dataset_extra_details= "Create more duplicate data during insert (INSERT INTO ...)",
#         exercise_extra_details ="The solution query must have following structure:" \
#         '''SELECT DISTINCT c
#             FROM ( SELECT col_1 [, col2 [,col_n]], COUNT(*) c
#                     FROM table
#                     GROUP BY col_1 [, col_2 [, col_n]] 
#             )''',
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(1),
#                 constraints.query.Distinct(),
#                 constraints.query.Aggregation(allowed_functions=["COUNT"]),
#                 constraints.query.NoHaving(),
#                 constraints.query.RequireSubqueries(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(allowed_functions=["COUNT"]),
#                 constraints.query.Distinct(),
#                 constraints.query.RequireSubqueries(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(allowed_functions=["COUNT"]),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Distinct()
#             ]
#         }
#     ),
#     SqlErrors.LOG_79_MISSING_DISTINCT_FROM_FUNCTION_PARAMETER: SqlErrorRequirements(
#         description="Missing DISTINCT from function parameter",
#         exercise_extra_details = "The exercise must NOT have PRIMARY KEY inside COUNT, "
#         "and must have DISTINCT inside COUNT",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Distinct(),
#                 constraints.query.Aggregation(allowed_functions=["COUNT"]),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(allowed_functions=["COUNT"]),
#                 constraints.query.Distinct(),
#                 constraints.query.HasUniqueKeyConstraint(state=False),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(allowed_functions=["COUNT"]),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Distinct(),
#                 constraints.query.HasUniqueKeyConstraint(state=False)
#             ]
#         }
#     ),
#     SqlErrors.LOG_80_INCORRECT_FUNCTION: SqlErrorRequirements(
#         description="Incorrect function",
#         exercise_extra_details ="The natural language query must be ambiguous to confuse the use of " \
#         "aggregate functions respect others (e.g. total can be SUM or COUNT).",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery(),           
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(3),
#                 constraints.query.RequireSubqueries()            
#             ]
#         }
#     ),
#     SqlErrors.LOG_81_INCORRECT_COLUMN_AS_FUNCTION_PARAMETER: SqlErrorRequirements(
#         description="Incorrect column as function parameter",
#         exercise_extra_details ="The natural language query must be ambiguous to confuse the student in the choice " \
#         "of columns that go into the functions.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),           
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery(),            
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(3),
#                 constraints.query.RequireSubqueries()            
#             ]
#         }
#     ),
#     SqlErrors.COM_83_UNNECESSARY_DISTINCT_IN_SELECT_CLAUSE: SqlErrorRequirements(
#         description="Unnecessary DISTINCT in SELECT clause",
#         exercise_extra_details ="In solution there must be no DISTINCT.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoDistinct(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoDistinct(),
#                 constraints.query.NoSubquery(),           
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(3),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.NoDistinct(),            
#             ]
#         }
#     ),
#     SqlErrors.COM_84_UNNECESSARY_JOIN: SqlErrorRequirements(
#         description="Unnecessary join",
#         dataset_extra_details ="In TABLE CREATION must be FOREIGN KEY relationship between tables ",
#         exercise_extra_details="In the solution query must be selected ONLY FOREIGN KEY column for at least one table in select.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery(),
#                 constraints.query.NoSubquery(),        
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(3),
#                 constraints.query.RequireSubqueries()            
#             ]
#         }
#     ),
#     SqlErrors.COM_86_CORRELATION_NAMES_ARE_ALWAYS_IDENTICAL: SqlErrorRequirements(
#         description="Correlation names are always identical",
#         dataset_extra_details="In the assignment create two table with same PRIMARY KEY with same name "
#         "(e.g. table 'tablename' with PK 'name_id' and table 'tablename_info' with PK 'name_id').",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(3),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(3),
#                 constraints.query.RequireSubqueries()           
#             ]
#         }
#     ),                         
#     SqlErrors.COM_88_LIKE_WITHOUT_WILDCARDS: SqlErrorRequirements(
#         description="LIKE without wildcards",
#         exercise_extra_details ="The natural language query you must confuse the student by making him " \
#         "believe that the LIKE keyword is necessary. In the solution MUST NOT HAVE LIKE and WILDCARDS.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(type=WhereConstraintType.NO_WILDCARD),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(type=WhereConstraintType.NO_WILDCARD),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(type=WhereConstraintType.NO_WILDCARD),
#                 constraints.query.Aggregation(3),
#                 constraints.query.RequireSubqueries()           
#             ]
#         }
#     ),
#     SqlErrors.COM_89_UNNECESSARILY_COMPLICATED_SELECT_IN_EXISTS_SUBQUERY: SqlErrorRequirements(
#         description="Unnecessarily complicated SELECT in EXISTS subquery",
#         exercise_extra_details ="In the solution must be EXISTS WITH only one column in SELECT and WITHOUT DISTINCT.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(type=WhereConstraintType.EXIST),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.NoDistinct(),
#                 constraints.query.NoHaving(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2, type=WhereConstraintType.EXIST),
#                 constraints.query.RequireSubqueries(2),
#                 constraints.query.NoDistinct()
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(3, type=WhereConstraintType.EXIST),
#                 constraints.query.Aggregation(3),
#                 constraints.query.RequireSubqueries(2),
#                 constraints.query.Distinct()           
#             ]
#         }
#     ),
#     SqlErrors.COM_91_UNNECESSARY_AGGREGATE_FUNCTION: SqlErrorRequirements(
#         description="Unnecessary aggregate function",
#         exercise_extra_details ="In natural language query use term as 'maximum', 'minimum', " \
#         "'count', 'average' ecc... that help to confuse the student but NOT use AGGREGATION.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoAggregation(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoAggregation(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.NoAggregation(),
#                 constraints.query.RequireSubqueries()           
#             ]
#         }
#     ),
#     SqlErrors.COM_93_UNNECESSARY_ARGUMENT_OF_COUNT: SqlErrorRequirements(
#         description="Unnecessary argument of COUNT",
#         exercise_extra_details ="In solution must be the aggregation count with a star -> COUNT(*) .",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(1),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(1),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(1),
#                 constraints.query.RequireSubqueries()           
#             ]
#         }
#     ),
#     SqlErrors.COM_95_GROUP_BY_WITH_SINGLETON_GROUPS: SqlErrorRequirements(
#         description="GROUP BY with singleton groups",
#         exercise_extra_details ="The solution MUST HAVE GROUP BY but on NON UNIQUE columns",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoAggregation(),
#                 constraints.query.GroupBy(1),
#                 constraints.query.NoDistinct(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoAggregation(),
#                 constraints.query.GroupBy(2),
#                 constraints.query.NoDistinct(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.NoAggregation(),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.GroupBy(3),
#                 constraints.query.NoDistinct()
#             ]
#         }
#     ),
#     SqlErrors.COM_96_GROUP_BY_WITH_ONLY_A_SINGLE_GROUP: SqlErrorRequirements(
#         description="GROUP BY with only a single group",
#         exercise_extra_details ="The solution must have in select ONLY aggregate functions.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.NoGroupBy(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(2),
#                 constraints.query.NoGroupBy(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.Aggregation(3),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.NoGroupBy()
#             ]
#         }
#     ),
#     SqlErrors.COM_97_GROUP_BY_CAN_BE_REPLACED_WITH_DISTINCT: SqlErrorRequirements(#controllare
#         description="GROUP BY can be replaced with DISTINCT",
#         exercise_extra_details ="In natural language query must create a query tahat can be solved with " \
#         "DISTINCT but the student can be confused to use GROUP BY.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoGroupBy(),
#                 constraints.query.Distinct(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.NoGroupBy(),
#                 constraints.query.Distinct(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.NoGroupBy(),
#                 constraints.query.Distinct()
#             ]
#         }
#     ),
#     SqlErrors.COM_98_UNION_CAN_BE_REPLACED_BY_OR: SqlErrorRequirements(#controllare
#         description="UNION can be replaced by OR",
#         exercise_extra_details ="The natural language query must have a request that can be solved with a " \
#         "single SELECT with OR in where condition or with UNION",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Union(state=False),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.Union(state=False),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation(),
#                 constraints.query.Union(state=False)
#             ]
#         }
#     ),
#     SqlErrors.COM_99_UNNECESSARY_COLUMN_IN_ORDER_BY_CLAUSE: SqlErrorRequirements(
#         description="Unnecessary column in ORDER BY clause",
#         exercise_extra_details ="In natural language query MUST BE AMBIGUOUS on the order of " \
#         "the result table in ORDER BY clause, dont use the world 'Sort' or 'Order'.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Union(state=False),
#                 constraints.query.OrderBy(2),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.Union(state=False),
#                 constraints.query.OrderBy(3),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation(),
#                 constraints.query.OrderBy(4)
#             ]
#         }
#     ),
#     SqlErrors.COM_102_INEFFICIENT_UNION: SqlErrorRequirements(
#         description="Inefficient UNION",
#         exercise_extra_details ="In the natural language query you need to create a case where use of " \
#         "UNION ALL or UNION should be used depending on what request is made. In solution " \
#         "if table in FROM are the same MUST USE UNION ALL, else if tables are different MUST USE UNION.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Union(state=True),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.Union(state=True),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation(),
#                 constraints.query.Union(state=True)
#             ]
#         }
#     ),
#     SqlErrors.COM_104_CONDITION_ON_LEFT_TABLE_IN_LEFT_OUTER_JOIN: SqlErrorRequirements(
#         description="Condition on left table in LEFT OUTER JOIN",
#         exercise_extra_details ="The natural language query must create ambiguity about which table " \
#         "the condition applies to.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Join(left=True),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.Join(left=True),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation(),
#                 constraints.query.Join(2, left=True)
#             ]
#         }
#     ),
#     SqlErrors.COM_105_OUTER_JOIN_CAN_BE_REPLACED_BY_INNER_JOIN: SqlErrorRequirements(#controllare
#         description="OUTER JOIN can be replaced by INNER JOIN",
#         exercise_extra_details ="he natural language query must create ambiguity about which JOIN " \
#         "to use with words like 'right' and 'left'.",
#         constraints={
#             DifficultyLevel.EASY: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Join(),
#                 constraints.query.NoHaving(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.MEDIUM: [
#                 constraints.query.HasWhereConstraint(2),
#                 constraints.query.Aggregation(),
#                 constraints.query.Join(),
#                 constraints.query.NoSubquery(),
#             ],
#             DifficultyLevel.HARD: [
#                 constraints.query.HasWhereConstraint(4),
#                 constraints.query.RequireSubqueries(),
#                 constraints.query.Aggregation(),
#                 constraints.query.Join(2)
#             ]
#         }
#     )
# }
