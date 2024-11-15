#!/usr/bin/env python

import progress.bar
import progress.colors
from pydantic import BaseModel

from dav_tools import argument_parser, messages, chatgpt, ArgumentAction

from misconceptions import Misconceptions

from progress.bar import IncrementalBar


class Assignment:
    def __init__(self, misconceptions: list[Misconceptions], language: str = 'PostgreSQL'):
        self.misconceptions = misconceptions
        self.language = language
        self.message = chatgpt.Message()

    def generate(self):
        with IncrementalBar('Generating assignment...', max=4, suffix='%(percent)d%% [%(index)d/%(max)d] - %(eta_td)s remaining') as progress:
            # messages.progress('Generating assignment...')
            self.generate_assignment()
            progress.next()

            # messages.progress('Generating solutions...')
            self.generate_task()
            progress.next()

            # messages.progress('Extracting schema...')
            self.generate_schema()
            progress.next()

            # messages.progress('Generating solutions...')
            self.generate_solutions()
            progress.next()

    def generate_assignment(self):
        misconceptions_descriptions = [misconception.value.description for misconception in self.misconceptions]
        misconceptions = '\n - '.join(misconceptions_descriptions)

        message = f'''Generate a SQL assignment asking students to write a specific {self.language} query.
The assignment should focus on the following misconception(s):
- {misconceptions}
'''

        self.message.add_message(chatgpt.MessageRole.USER, message)
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o)

    def generate_schema(self):
        message = f'''Return the schema, formatted as a {self.language} CREATE TABLE script'''
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o)
    
    def generate_solutions(self):
        class Solution(BaseModel):
            correct_solution: str
            wrong_solution: str

            def __str__(self):
                return f'''=== CORRECT ===\n{self.correct_solution}\n\n=== WRONG ===\n{self.wrong_solution}'''

        message = f'''Return the correct solution, as well as the expected wrong solution containing the misconception. Print only the {self.language} code.'''
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o, json_format=Solution)

    def generate_task(self):
        message = f'''Return the task, i.e. the query request in natural language'''
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o)


if __name__ == '__main__':
    argument_parser.set_developer_info('Davide Ponzini', 'davide.ponzini@edu.unige.it')
    argument_parser.set_description('Generate SQL assignments based on specific misconceptions')
    argument_parser.args

    misconceptions = [
        Misconceptions.COM_1_COMPLICATION_ORDER_BY_IN_SUBQUERY,
    ]
    assignment = Assignment(misconceptions)

    for misconception in misconceptions:
        messages.info(f'Misconception: {misconception.name}')

    assignment.generate()
    assignment.message.print()
