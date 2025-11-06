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
    def generate_from_ai_html(cls, domain, error_details, difficulty) -> AssignmentFormat:

        constraints_list = error_details.constraints[difficulty]
        formatted_constraints = "\n".join(f"- {item}" for item in constraints_list)

        assignment_text = f"""
            Progetta un esercizio SQL completo che tratta di un dominio di tipo {domain}. Che insegna a risolvere query che potrebbero
            causare errori come {error_details.description} che deve avere le seguenti caratteristiche: {error_details.characteristics}.
            In oltre si DEVONO rispettare i seguenti vincoli:
            {formatted_constraints}

            Segui ESATTAMENTE questa struttura JSON per la tua risposta:
            {{
                "schema": ["CREATE TABLE comando 1...", "CREATE TABLE comando 2..."],
                "request": "La richiesta per lo studente in linguaggio naturale.",
                "solution": "La singola query SQL corretta come soluzione."
            }}
            """ 

        chat = chatgpt.Message()
        chat.add_message(chatgpt.MessageRole.USER, assignment_text)
        answer = chat.generate_answer(
            model=chatgpt.AIModel.GPT4o_mini,
            json_format=AssignmentFormat
        )

        if not isinstance(answer, AssignmentFormat):
            raise TypeError(f"La risposta dell'AI non è stata convertita in un oggetto AssignmentFormat. Controllare la libreria dav_tools. Risposta ricevuta: {type(answer)}")

        return answer
    










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