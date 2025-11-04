from pydantic import BaseModel
from progress.bar import IncrementalBar

from dav_tools import messages, chatgpt

from misconceptions import Misconceptions
import util


class AssignmentSolution(BaseModel):
    correct: str
    wrong: str

    def __str__(self):
        return f'''=== CORRECT ===
{self.correct}

=== WRONG ===
{self.wrong}'''


class Assignment:
    def __init__(self, misconceptions: list[Misconceptions], language: str = 'PostgreSQL', topic: None | str = None):
        assert len(misconceptions) > 0, 'No misconceptions provided'

        self.misconceptions = misconceptions
        self.language = language
        self.topic = topic

        self.message = chatgpt.Message()
        
        self.schema: str = None
        self.task: str = None
        self.solution: AssignmentSolution = None

    def generate(self):
        with IncrementalBar('Generating assignment...', max=4, suffix='%(percent)d%% [%(index)d/%(max)d] - %(eta_td)s remaining') as progress:
            # messages.progress('Generating assignment...')
            self._generate_assignment()
            progress.next()

            # messages.progress('Generating solutions...')
            self._generate_task()
            progress.next()

            # messages.progress('Extracting schema...')
            self._generate_schema()
            progress.next()

            # messages.progress('Generating solutions...')
            self._generate_solutions()
            progress.next()

    def _generate_assignment(self):
        misconceptions_descriptions = '\n'.join([f'- {misconception.value.description}' for misconception in self.misconceptions])

        message = f'''
            Generate an assignment asking students to write exactly one {self.language} query.
            The assignment should focus on the following misconception(s):
            {misconceptions_descriptions}
            
            The assignment has to be designed in order to trigger the misconception(s) in students, so that the teacher could then explain them.
        '''

        if self.topic is not None:
            message += f'''
                The assignment should revolve about the following topic: {self.topic}.
            '''

        misconceptions_requirements = []
        for misconception in self.misconceptions:
            for requirement in misconception.value.requirements:
                misconceptions_requirements.append(requirement)

        if len(misconceptions_requirements) > 0:
            misconceptions_requirements = '\n'.join([f'- {req}' for req in misconceptions_requirements])

            message += f'''
                Also, you must respect the following requirement(s) when creating the assignment:
                {misconceptions_requirements}
            '''
        
        message = util.strip_lines(message)

        self.message.add_message(chatgpt.MessageRole.USER, message)
        self.message.generate_answer(model=chatgpt.AIModel.GPT4o)

    def _generate_task(self):
        message = f'''
            Return the task, i.e. the query request in natural language.
            Formulate the query in a simple way, without providing hints as to how it should be solved.
        '''
        message = util.strip_lines(message)
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        self.task = self.message.generate_answer(model=chatgpt.AIModel.GPT4o)

    def _generate_schema(self):
        message = f'''
            Provide the schema, formatted as a {self.language} CREATE TABLE script.
            Return only the {self.language} code and nothing else
        '''
        message = util.strip_lines(message)

        self.message.add_message(chatgpt.MessageRole.USER, message)
        schema = self.message.generate_answer(model=chatgpt.AIModel.GPT4o)

        schema = util.extract_sql(schema)
        
        if schema is None:
            messages.error('Schema generation failed')
            return
        
        self.schema = schema

    
    def _generate_solutions(self):
        message = f'''
            Return the correct solution in JSON format, as well as the expected wrong solution containing the misconception. Print only the {self.language} code.
        '''
        message = util.strip_lines(message)
        
        self.message.add_message(chatgpt.MessageRole.USER, message)
        self.solution = self.message.generate_answer(model=chatgpt.AIModel.GPT4o, json_format=AssignmentSolution)

