#!/usr/bin/env python

import pyperclip
from pydantic import BaseModel

from dav_tools import argument_parser, messages, chatgpt, ArgumentAction

from misconceptions import Misconceptions


class Assignment:
    def __init__(self, misconception: Misconceptions, language: str = 'PostgreSQL'):
        self.misconception = misconception
        self.language = language
        self.message = chatgpt.Message()

    def generate_assignment(self):
        message = f'''Generate a SQL assignment asking students to write a specific {self.language} query.
    The assignment should focus on the following misconception: {self.misconception.value.description}.'''

        self.message.add_message(chatgpt.MessageRole.USER, message)
        messages.progress('Generating assignment...')
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o)

    def extract_schema(self):
        message = f'''Return the schema, formatted as a {self.language} CREATE TABLE script'''
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        messages.progress('Extracting schema...')
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o)
    
    def extract_solutions(self):
        class Solution(BaseModel):
            correct_solution: str
            wrong_solution: str

            def __str__(self):
                return f'''=== CORRECT ===\n{self.correct_solution}\n\n=== WRONG ===\n{self.wrong_solution}'''

        message = f'''Return the correct solution, as well as the expected wrong solution containing the misconception. Print only the {self.language} code.'''
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        messages.progress('Generating solutions...')
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o, json_format=Solution)

    def extract_task(self):
        message = f'''Return the task, i.e. the query request in natural language'''
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        messages.progress('Generating solutions...')
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o)


if __name__ == '__main__':
    misconception = Misconceptions.SEM_1_INCONSISTENT_EXPRESSION_DISTINCT_IN_SUM_OR_AVG
    assignment = Assignment(misconception)

    messages.info(f'Misconception: {misconception.name}')
    assignment.generate_assignment()
    assignment.extract_task()
    assignment.extract_schema()
    assignment.extract_solutions()
    assignment.message.print()
