from __future__ import annotations
from dataclasses import dataclass
from dav_tools import chatgpt, messages
from .assignment_answer_format import AssignmentFormat
from .query_sintax import is_solution_valid


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

        ### GUIDELINES ###
        Generate SQL exercise with domain: {domain}. 
        The exercise should NATURALLY tempts student to write a query that fails due to {error_details.description}. 
        The exercise must have the characteristics: {error_details.characteristics}.
        
        ### MANDATORY REQUIREMENTS FOR THE EXERCISE ###
        {formatted_constraints}
        
        #### JSON REQUIRED OUTPUT FORMAT ####
        {{
            "schema": ["CREATE TABLE command 1...", "CREATE TABLE command 2..."] can create more table than the students need,
            "request": "Extract and return ONLY NATURAL LANGUAGE query following the assigned constraints. NEVER ask to include mistake.",
            "solution": "Only a single, correct, and executable SQL query following the ASSIGNED CONNSTRAINTS. The query must be well-formatted."
        }}
        """

        chat = chatgpt.Message()
        chat.add_message(chatgpt.MessageRole.USER, assignment_text)

        for attempt in range(3):
            print(f"---> Attempt {attempt + 1} of {3}...")
            
            answer = chat.generate_answer(
                model=chatgpt.AIModel.GPT4o_mini,
                json_format=AssignmentFormat,
                add_to_messages=False
            )

            if not isinstance(answer, AssignmentFormat):
                raise TypeError(f"The answer is not type format AssignmentFormat: {type(answer)}")

            is_valid, missing = is_solution_valid(answer.schemas, answer.solution, constraints_list)
            if is_valid:
                print("---> Generated assignment is valid. Success!")
                return answer
            else:
                print(f"---> Validation failed. Missing requirements: {', '.join(missing)}")
                feedback = (
                    f"The previously SQL solution was WRONG because it was MISSING: {', '.join(missing)}. "
                    f"""Please regenerate the exercise with JSON format like previous request, 
                    the new SQL query must follows ALL the original mandatory requirements: {formatted_constraints}""")
                
                chat.add_message(chatgpt.MessageRole.ASSISTANT, answer.model_dump_json())
                chat.add_message(chatgpt.MessageRole.USER, feedback)

        raise Exception(f"Failed to generate a valid assignment after {3} attempts.")