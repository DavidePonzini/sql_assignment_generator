#!/usr/bin/env python


from dav_tools import argument_parser, messages

from assignment import Assignment
from misconceptions import Misconceptions


if __name__ == '__main__':
    argument_parser.set_developer_info('Davide Ponzini', 'davide.ponzini@edu.unige.it')
    argument_parser.set_description('Generate SQL assignments based on specific misconceptions')
    argument_parser.add_verbose_mode()
    argument_parser.add_argument('--topic', help='Assignment topic')
    argument_parser.args

    misconceptions = [
        # Misconceptions.SEM_1_INCONSISTENT_EXPRESSION_AND_INSTEAD_OF_OR,                                         # 39
        Misconceptions.SEM_1_INCONSISTENT_EXPRESSION_TAUTOLOGICAL_OR_INCONSISTENT_EXPRESSION,                   # 40
        # Misconceptions.SEM_1_INCONSISTENT_EXPRESSION_DISTINCT_IN_SUM_OR_AVG,                                    # 41
        # Misconceptions.SEM_1_INCONSISTENT_EXPRESSION_DISTINCT_THAT_MIGHT_REMOVE_IMPORTANT_DUPLICATES,           # 42
        # Misconceptions.SEM_1_INCONSISTENT_EXPRESSION_WILDCARDS_WITHOUT_LIKE,                                    # 43
        # Misconceptions.SEM_1_INCONSISTENT_EXPRESSION_INCORRECT_WILDCARD_USING_UNDERSCORE_INSTEAD_OF_PERCENT,    # 44
        # Misconceptions.SEM_2_INCONSISTENT_JOIN_NULL_IN_IN_ANY_ALL_SUBQUERY,                                     # 46
    ]

    misconceptions_list = '\n'.join([f'{misconception.value.id:3}. {misconception.name}: {req}' for misconception in misconceptions for req in misconception.value.requirements])
    messages.message(f'\n{misconceptions_list}',            icon='Misconceptions & requirements', icon_options=[messages.TextFormat.Color.RED])
    messages.ask_continue(default_yes=True)

    assignment = Assignment(misconceptions, topic=argument_parser.args.topic)
    assignment.generate()

    if argument_parser.is_verbose:
        assignment.message.print()

    misconceptions_list = '\n'.join([f'{misconception.value.id:3}. {misconception.name}: {req}' for misconception in misconceptions for req in misconception.value.requirements])

    messages.message(f'\n{assignment.schema}',              icon='Schema', icon_options=[messages.TextFormat.Color.RED])
    messages.message(f'\n{assignment.task}',                icon='Task', icon_options=[messages.TextFormat.Color.RED])
    messages.message(f'\n{assignment.solution.correct}',    icon='Solution - correct', icon_options=[messages.TextFormat.Color.RED])
    messages.message(f'\n{assignment.solution.wrong}',      icon='Solution - wrong', icon_options=[messages.TextFormat.Color.RED])
