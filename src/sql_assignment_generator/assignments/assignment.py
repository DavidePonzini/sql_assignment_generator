from __future__ import annotations
from dataclasses import dataclass
from dav_tools import chatgpt, messages
from .assignment_answer_format import AssignmentFormat

@dataclass
class Assignment:
    request: str
    solution: str
    schema: str

    @classmethod
    def generate_text(cls, domain, error_details, difficulty) -> Assignment:
        
        constraints_list = error_details.constraints[difficulty]
        formatted_constraints = "\n".join(f"- {item}" for item in constraints_list)
        
        assignment_text = f"""
            Design a complete SQL exercise that deals with a domain of type {domain}. 
            The exercise should present a scenario that naturally tempts a student to write a query 
            that fails due to {error_details.description}. 
            The exercise must have the following characteristics: {error_details.characteristics}.
            Create more table than the students need but only one query solution. 
            Mandatory constraints to must be respect in the exercise: {formatted_constraints}
        """

        # print("----------------------------------------------------------------------------------------------------------------")
        # print(assignment_text)
        # print("----------------------------------------------------------------------------------------------------------------")


        #IA call
        chat = chatgpt.Message()
        chat.add_message(chatgpt.MessageRole.USER, assignment_text)
        full_response = chat.generate_answer(model=chatgpt.AIModel.GPT4o_mini)


        #RETURN SCHEMA
        chat_schema = chatgpt.Message()
        schema_prompt = (
            f"Basing on this generated exercise:\n---\n{full_response}\n---\n"
            "Extract and return ONLY the table in format 'CREATE TABLE' following the assigned constraints"
        )
        chat_schema.add_message(chatgpt.MessageRole.USER, schema_prompt)
        schema_part = chat_schema.generate_answer(model=chatgpt.AIModel.GPT4o_mini)


        #RETURN REQUEST
        chat_request = chatgpt.Message()
        request_prompt = (
            f"Basing on this exercise:\n---\n{full_response}\n---\n"
            f"And having this table:\n---\n{schema_part}\n---\n"
            "Extract and return ONLY NATURAL LANGUAGE query following assigned constraints."
        )
        chat_request.add_message(chatgpt.MessageRole.USER, request_prompt)
        request_part = chat_request.generate_answer(model=chatgpt.AIModel.GPT4o_mini)


        #RETURN SOLUTION
        chat_solution = chatgpt.Message()
        solution_prompt = (
            f"Basing on this exercise:\n---\n{full_response}\n---\n"
            f"And having this natural language request:\n---\n{request_part}\n---\n"
            "Return ONLY a single, correct, well-formatted and executable SQL query following the ASSIGNED CONNSTRAINTS."
        )
        chat_solution.add_message(chatgpt.MessageRole.USER, solution_prompt)
        solution_part = chat_solution.generate_answer(model=chatgpt.AIModel.GPT4o_mini)

        return cls(
            schema=schema_part,
            request=request_part,
            solution=solution_part
        )

    def print_assignment(self):
        messages.message(f'\n{self.schema}', icon='Schema', icon_options=[messages.TextFormat.Color.BLUE])
        messages.message(f'\n{self.request}', icon='Request', icon_options=[messages.TextFormat.Color.BLUE])
        messages.message(f'\n{self.solution}',icon='Solution', icon_options=[messages.TextFormat.Color.BLUE])

    


    @classmethod
    def generate_textFormat(cls, domain, error_details, difficulty) -> AssignmentFormat:

        constraints_list = error_details.constraints[difficulty]
        formatted_constraints = "\n".join(f"- {item}" for item in constraints_list)

        assignment_text =f"""
        Design a complete SQL exercise that deals with a domain of type {domain}. 
        The exercise should present a scenario that naturally tempts a student to write a query 
        that fails due to {error_details.description}. 
        The exercise must have the following characteristics: {error_details.characteristics}.
        Create more table than the students need to solve exercise but only one query solution.
        You must respect ALL the following mandatory exercise constraints:
        {formatted_constraints}
        
        Follow EXACTLY this JSON structure for your response:
        {{
            "schema": ["CREATE TABLE command 1...", "CREATE TABLE command 2..."],
            "request": "Extract and return ONLY NATURAL LANGUAGE query following the assigned constraints. NEVER ask to include mistake.",
            "solution": "Only a single, correct, and executable SQL query following the ASSIGNED CONNSTRAINTS. The query must be well-formatted."
        }}
        """

        #print(assignment_text)

        chat = chatgpt.Message()
        chat.add_message(chatgpt.MessageRole.USER, assignment_text)
        answer = chat.generate_answer(
            model=chatgpt.AIModel.GPT4o_mini,
            json_format=AssignmentFormat
        )

        if not isinstance(answer, AssignmentFormat):
            raise TypeError(f"The answer is not type format AssignmentFormat: {type(answer)}")

        return answer