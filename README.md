# sql-assignment-generation
Automated generation of SQL assignments based on misconceptions.

# Misconceptions - To Do List

## Syntax errors

### Ambiguous Database Object

1. [ ] **syn_1_ambiguous_database_object_omitting_correlation_names**
2. [ ] **syn_1_ambiguous_database_object_ambiguous_column**
3. [ ] **syn_1_ambiguous_database_object_ambiguous_function**

### Undefined Database Object

4. [ ] **syn_2_undefined_database_object_undefined_column**
5. [ ] **syn_2_undefined_database_object_undefined_function**
6. [ ] **syn_2_undefined_database_object_undefined_parameter**
7. [ ] **syn_2_undefined_database_object_undefined_object**
8. [ ] **syn_2_undefined_database_object_invalid_schema_name**
9. [ ] **syn_2_undefined_database_object_misspellings**
10. [ ] **syn_2_undefined_database_object_synonyms**
11. [ ] **syn_2_undefined_database_object_omitting_quotes_around_character_data**

### Data Type Mismatch

12. [ ] **syn_3_data_type_mismatch_failure_to_specify_column_name_twice**
13. [ ] **syn_3_data_type_mismatch**

### Illegal Aggregate Function Placement

14. [ ] **syn_4_illegal_aggregate_function_placement_using_aggregate_function_outside_select_or_having**
15. [ ] **syn_4_illegal_aggregate_function_placement_grouping_error_aggregate_functions_cannot_be_nested**

### Illegal or Insufficient Grouping

16. [ ] **syn_5_illegal_or_insufficient_grouping_grouping_error_extraneous_or_omitted_grouping_column**
17. [ ] **syn_5_illegal_or_insufficient_grouping_strange_having_having_without_group_by**

### Common Syntax Error

18. [ ] **syn_6_common_syntax_error_confusing_function_with_function_parameter**
19. [ ] **syn_6_common_syntax_error_using_where_twice**
20. [ ] **syn_6_common_syntax_error_omitting_the_from_clause**
21. [ ] **syn_6_common_syntax_error_comparison_with_null**
22. [ ] **syn_6_common_syntax_error_omitting_the_semicolon**
23. [ ] **syn_6_common_syntax_error_date_time_field_overflow**
24. [ ] **syn_6_common_syntax_error_duplicate_clause**
25. [ ] **syn_6_common_syntax_error_using_an_undefined_correlation_name**
26. [ ] **syn_6_common_syntax_error_too_many_columns_in_subquery**
27. [ ] **syn_6_common_syntax_error_confusing_table_names_with_column_names**
28. [ ] **syn_6_common_syntax_error_restriction_in_select_clause**
29. [ ] **syn_6_common_syntax_error_projection_in_where_clause**
30. [ ] **syn_6_common_syntax_error_confusing_the_order_of_keywords**
31. [ ] **syn_6_common_syntax_error_confusing_the_logic_of_keywords**
32. [ ] **syn_6_common_syntax_error_confusing_the_syntax_of_keywords**
33. [ ] **syn_6_common_syntax_error_omitting_commas**
34. [ ] **syn_6_common_syntax_error_curly_square_or_unmatched_brackets**
35. [ ] **syn_6_common_syntax_error_is_where_not_applicable**
36. [ ] **syn_6_common_syntax_error_nonstandard_keywords_or_standard_keywords_in_wrong_context**
37. [ ] **syn_6_common_syntax_error_nonstandard_operators**
38. [ ] **syn_6_common_syntax_error_additional_semicolon**

## Semantic Errors

### Inconsistent Expression

39. [x] **sem_1_inconsistent_expression_and_instead_of_or**
40. [ ] **sem_1_inconsistent_expression_tautological_or_inconsistent_expression**
41. [x] **sem_1_inconsistent_expression_distinct_in_sum_or_avg**
42. [x] **sem_1_inconsistent_expression_distinct_that_might_remove_important_duplicates**
43. [x] **sem_1_inconsistent_expression_wildcards_without_like**
44. [x] **sem_1_inconsistent_expression_incorrect_wildcard_using_underscore_instead_of_percent**
45. [ ] **sem_1_inconsistent_expression_mixing_a_greater_than_0_with_is_not_null**

### Inconsistent Join

46. [ ] **sem_2_inconsistent_join_null_in_subquery**
47. [ ] **sem_2_inconsistent_join_join_on_incorrect_column**

### Missing Join

48. [ ] **sem_3_missing_join_omitting_a_join**

### Duplicate Rows

49. [ ] **sem_4_duplicate_rows_many_duplicates**

### Redundant Column Output

50. [ ] **sem_5_redundant_column_output_constant_column_output**
51. [ ] **sem_5_redundant_column_output_duplicate_column_output**

## Logical Errors

### Operator Error

52. [ ] **log_1_operator_error_or_instead_of_and**
53. [ ] **log_1_operator_error_extraneous_not_operator**
54. [ ] **log_1_operator_error_missing_not_operator**
55. [ ] **log_1_operator_error_substituting_existence_negation_with_not_equal_to**
56. [ ] **log_1_operator_error_putting_not_in_front_of_incorrect_in_or_exists**
57. [ ] **log_1_operator_error_incorrect_comparison_operator_or_value**

### Join Error

58. [ ] **log_2_join_error_join_on_incorrect_table**
59. [ ] **log_2_join_error_join_when_join_needs_to_be_omitted**
60. [ ] **log_2_join_error_join_on_incorrect_column_matches_possible**
61. [ ] **log_2_join_error_join_with_incorrect_comparison_operator**
62. [ ] **log_2_join_error_missing_join**

### Nesting Error

63. [ ] **log_3_nesting_error_improper_nesting_of_expressions**
64. [ ] **log_3_nesting_error_improper_nesting_of_subqueries**

### Expression Error

65. [ ] **log_4_expression_error_extraneous_quotes**
66. [ ] **log_4_expression_error_missing_expression**
67. [ ] **log_4_expression_error_expression_on_incorrect_column**
68. [ ] **log_4_expression_error_extraneous_expression**
69. [ ] **log_4_expression_error_expression_in_incorrect_clause**

### Projection Error

70. [ ] **log_5_projection_error_extraneous_column_in_select**
71. [ ] **log_5_projection_error_missing_column_from_select**
72. [ ] **log_5_projection_error_missing_distinct_from_select**
73. [ ] **log_5_projection_error_missing_as_from_select**
74. [ ] **log_5_projection_error_missing_column_from_order_by**
75. [ ] **log_5_projection_error_incorrect_column_in_order_by**
76. [ ] **log_5_projection_error_extraneous_order_by_clause**
77. [ ] **log_5_projection_error_incorrect_ordering_of_rows**

### Function Error

78. [ ] **log_6_function_error_distinct_as_function_parameter_where_not_applicable**
79. [ ] **log_6_function_error_missing_distinct_from_function_parameter**
80. [ ] **log_6_function_error_incorrect_function**
81. [ ] **log_6_function_error_incorrect_column_as_function_parameter**

## Complications

82. [ ] **com_1_complication_unnecessary_complication**
83. [ ] **com_1_complication_unnecessary_distinct_in_select_clause**
84. [ ] **com_1_complication_unnecessary_join**
85. [ ] **com_1_complication_unused_correlation_name**
86. [ ] **com_1_complication_correlation_names_are_always_identical**
87. [ ] **com_1_complication_unnecessarily_general_comparison_operator**
88. [ ] **com_1_complication_like_without_wildcards**
89. [ ] **com_1_complication_unnecessarily_complicated_select_in_exists_subquery**
90. [ ] **com_1_complication_in_exists_can_be_replaced_by_comparison**
91. [ ] **com_1_complication_unnecessary_aggregate_function**
92. [ ] **com_1_complication_unnecessary_distinct_in_aggregate_function**
93. [ ] **com_1_complication_unnecessary_argument_of_count**
94. [ ] **com_1_complication_unnecessary_group_by_in_exists_subquery**
95. [ ] **com_1_complication_group_by_with_singleton_groups**
96. [ ] **com_1_complication_group_by_can_be_replaced_with_distinct**
97. [ ] **com_1_complication_union_can_be_replaced_by_or**
98. [ ] **com_1_complication_unnecessary_column_in_order_by_clause**
99. [ ] **com_1_complication_order_by_in_subquery**
100. [ ] **com_1_complication_inefficient_having**
101. [ ] **com_1_complication_inefficient_union**
102. [ ] **com_1_complication_condition_in_subquery_can_be_moved_up**
103. [ ] **com_1_complication_condition_on_left_table_in_left_outer_join**
104. [ ] **com_1_complication_outer_join_can_be_replaced_by_inner_join**
105. [ ] **com_x_complication_join_condition_in_where_clause**
