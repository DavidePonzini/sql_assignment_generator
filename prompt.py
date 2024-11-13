#!/usr/bin/env python

from dav_tools import argument_parser, messages, chatgpt, ArgumentAction
import pyperclip

from misconceptions import Misconceptions


class AssignmentPrompt:
    def __init__(self, misconception: Misconceptions, language: str = 'PostgreSQL'):
        self.misconception = misconception
        self.language = language
        self.message = chatgpt.Message()

    def generate_assignment(self):
        self._add_prompt_generate_assignment()

        messages.progress('Generating assignment...')
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o, require_json=False)

    def _add_prompt_generate_assignment(self):
        message = f'''Generate a SQL assignment asking students to write a specific {self.language} query.
    The assignment should focus on the following misconception: {self.misconception.value.description}.
'''

        self.message.add_message(chatgpt.MessageRole.USER, message)
    
    def extract_schema(self):
        message = f'''Return the schema, formatted as a {self.language} CREATE TABLE script'''
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        messages.progress('Extracting schema...')
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o, require_json=False)
    
    def extract_solutions(self):
        message = f'''Return the correct solution, as well as the expected wrong solution containing the misconception'''
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        messages.progress('Generating solutions...')
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o, require_json=False)

    def extract_task(self):
        message = f'''Return the task, i.e. the query request in natural language'''
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        messages.progress('Generating solutions...')
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o, require_json=False)


if __name__ == '__main__':
    # argument_parser.add_argument('query', help='File containing query request in natural language')
    # argument_parser.add_argument('tables', help='File containing CREATE TABLE commands')
    # argument_parser.add_argument('values', nargs='?', help='File containing INSERT INTO commands')
    argument_parser.add_argument('--generate', action=ArgumentAction.STORE_TRUE, help='Generate the answer and print the result. If not set, print the prompt to screen')

    argument_parser.args

    assignment = AssignmentPrompt(Misconceptions.SEM_1_INCONSISTENT_EXPRESSION_DISTINCT_IN_SUM_OR_AVG)

    # if no model is specified, copy the prompt for manual execution
    if not argument_parser.args.generate:
        prompt = assignment._add_prompt_generate_assignment()
        pyperclip.copy(prompt)
        messages.info(prompt)
        messages.success('Prompt copied to clipboard')
        exit(0)

    # if a model is specified, generate the answer and show it
    assignment.generate_assignment()
    assignment.extract_task()
    assignment.extract_schema()
    assignment.extract_solutions()
    assignment.message.print()
