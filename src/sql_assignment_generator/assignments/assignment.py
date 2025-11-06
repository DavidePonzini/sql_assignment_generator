from __future__ import annotations
from dataclasses import dataclass
from dav_tools import chatgpt
from .assignment_answer_format import AssignmentFormat

@dataclass
class Assignment:
    request: str
    solution: str
    schema: str

    @classmethod
    def generate_from_ai_text(cls, domain, error_details, difficulty) -> AssignmentFormat:

        constraints_list = error_details.constraints[difficulty]
        formatted_constraints = "\n".join(f"- {item}" for item in constraints_list)

        assignment_text = f"""
        Design a complete SQL exercise that deals with a domain of type {domain}. It should teach how to solve queries that might
        cause errors like {error_details.description} and must have the following characteristics: {error_details.characteristics}.
        Furthermore, the following constraints MUST be respected:
        {formatted_constraints}
        
        Follow EXACTLY this JSON structure for your response:
        {{
            "schema": ["CREATE TABLE command 1...", "CREATE TABLE command 2..."],
            "request": "The request for the student in natural language.",
            "solution": "The single correct SQL query as the solution."
        }}
        """ 

        chat = chatgpt.Message()
        chat.add_message(chatgpt.MessageRole.USER, assignment_text)
        answer = chat.generate_answer(
            model=chatgpt.AIModel.GPT4o_mini,
            json_format=AssignmentFormat
        )

        if not isinstance(answer, AssignmentFormat):
            raise TypeError(f"The answer is not type format AssignmentFormat: {type(answer)}")

        return answer
    








#multy answer 

# from __future__ import annotations
# from dataclasses import dataclass
# from dav_tools import chatgpt, messages

# from .assignment_answer_format import AssignmentFormat

# @dataclass
# class Assignment:
#     request: str
#     solution: str
#     schema: str

    # @classmethod
    # def generate_from_ai_text(cls, domain, error_details, difficulty) -> Assignment:
        
    #     # - Use this keyword: {error_details.keywords}
    #     assignment_text = f"""
    #         Generate a complete SQL exercise based on the following details:
    #         - Domain: {domain}
    #         - Difficulty: {difficulty.name}
    #         - Error to learn to solve: {error_details.description}
    #         - Characteristics of exercise: {error_details.characteristics}
    #         - Constraints to must be respect in exercise: {error_details.constraints[difficulty]}
    #         """

    #     # print("----------------------------------------------------------------------------------------------------------------")
    #     # print(assignment_text)
    #     # print("----------------------------------------------------------------------------------------------------------------")


    #     #IA call
    #     chat = chatgpt.Message()
    #     chat.add_message(chatgpt.MessageRole.USER, assignment_text)
    #     full_response = chat.generate_answer(model=chatgpt.AIModel.GPT4o_mini)


        # #RETURN SCHEMA
        # chat_schema = chatgpt.Message()
        # schema_prompt = (
        #     f"Basandoti su questo scenario di esercizio:\n---\n{full_response}\n---\n"
        #     "Estrai e restituisci SOLO i comandi 'CREATE TABLE'"
        # )
        # chat_schema.add_message(chatgpt.MessageRole.USER, schema_prompt)
        # schema_part = chat_schema.generate_answer(model=chatgpt.AIModel.GPT4o_mini)


        # #RETURN REQUEST
        # chat_request = chatgpt.Message()
        # request_prompt = (
        #     f"Basandoti su questo scenario di esercizio:\n---\n{full_response}\n---\n"
        #     "Estrai e restituisci SOLO la richiesta per lo studente in linguaggio naturale."
        # )
        # chat_request.add_message(chatgpt.MessageRole.USER, request_prompt)
        # request_part = chat_request.generate_answer(model=chatgpt.AIModel.GPT4o_mini).strip()


        # #RETURN SOLUTION
        # chat_solution = chatgpt.Message()
        # solution_prompt = (
        #     f"Basandoti su questo scenario di esercizio:\n---\n{full_response}\n---\n"
        #     "Estrai e restituisci SOLO la query SQL di soluzione corretta."
        # )
        # chat_solution.add_message(chatgpt.MessageRole.USER, solution_prompt)
        # solution_part = chat_solution.generate_answer(model=chatgpt.AIModel.GPT4o_mini).strip()

    #     #return element
    #     return cls(
    #         schema=schema_part,
    #         request=request_part,
    #         solution=solution_part
    #     )

    # def print_assignment(self):
    #     messages.message(f'\n{self.schema}', icon='Schema', icon_options=[messages.TextFormat.Color.RED])
    #     messages.message(f'\n{self.request}', icon='Request', icon_options=[messages.TextFormat.Color.RED])
    #     messages.message(f'\n{self.solution}',icon='Solution', icon_options=[messages.TextFormat.Color.RED])