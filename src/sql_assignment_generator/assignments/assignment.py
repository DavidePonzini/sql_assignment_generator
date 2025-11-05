from __future__ import annotations
from dataclasses import dataclass
from dav_tools import messages, chatgpt
# La funzione è importata correttamente qui
from .assignment_answer_format import SchemaResponse, RequestResponse, SolutionResponse, _generate_json_part

@dataclass
class Assignment:
    request: str
    solution: str
    schema: str

    def print_assignment(self):
        messages.message(f'\n{self.schema}', icon='Schema', icon_options=[messages.TextFormat.Color.RED])
        messages.message(f'\n{self.request}', icon='Request', icon_options=[messages.TextFormat.Color.RED])
        messages.message(f'\n{self.solution}',icon='Solution', icon_options=[messages.TextFormat.Color.RED])

    @classmethod
    def generate_from_ai_json(cls, domain, error_details, difficulty) -> Assignment:

        constraints_list = error_details.constraints[difficulty]
        formatted_constraints = "\n".join(f"- {item}" for item in constraints_list)
        
        assignment_text = f"""
            Progetta un esercizio SQL completo che tratta di un dominio di tipo {domain}. Che insegna a risolvere query che potrebbero
            causare errori come {error_details.description} che deve avere le seguenti caratteristiche: {error_details.characteristics}.
            In oltre si DEVONO rispettare i seguenti vincoli:
            {formatted_constraints}
            """ 

        chat = chatgpt.Message()
        chat.add_message(chatgpt.MessageRole.USER, assignment_text)
        exercise_concept = chat.generate_answer(model=chatgpt.AIModel.GPT4o_mini)

        schema_part_list = _generate_json_part(
            base_context=exercise_concept,
            instruction="Genera SOLO lo schema SQL (istruzioni CREATE TABLE). La tua risposta DEVE essere un oggetto JSON con una singola chiave 'schema' che contiene una lista di stringhe.",
            response_model=SchemaResponse
        )
        # Unisci la lista di comandi in una singola stringa, separati da un a capo.
        schema_part = "\n".join(schema_part_list)

        request_part = _generate_json_part(
            base_context=exercise_concept,
            instruction="Genera SOLO la richiesta per lo studente in linguaggio naturale. La tua risposta DEVE essere un oggetto JSON con una singola chiave 'request'.",
            response_model=RequestResponse
        )

        solution_part = _generate_json_part(
            base_context=exercise_concept,
            instruction="Genera SOLO la query SQL corretta che risolve l'esercizio. La tua risposta DEVE essere un oggetto JSON con una singola chiave 'solution'.",
            response_model=SolutionResponse
        )
        # --- FINE MODIFICHE ---

        return cls(
            schema=schema_part,
            request=request_part,
            solution=solution_part
        )
    












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

    #         Please format your response EXACTLY as follows, using the specified separators:

    #         ---SCHEMA---
    #         [Return only the table schema to use in the format: CREATE TABLE 'tableName' ('TableField');]

    #         ---REQUEST---
    #         [Return only a clear natural language query describing the data to retrieve, without mentioning errors or hint]

    #         ---SOLUTION---
    #         [Return only the correct resulting query. The query must be executable without error.]
    #         """

    #     # print("----------------------------------------------------------------------------------------------------------------")
    #     # print(assignment_text)
    #     # print("----------------------------------------------------------------------------------------------------------------")


    #     #IA call
    #     chat = chatgpt.Message()
    #     chat.add_message(chatgpt.MessageRole.USER, assignment_text)
    #     full_response = chat.generate_answer(model=chatgpt.AIModel.GPT4o_mini) #json_format dopo model

    #     #divide the response in elment
    #     try:
    #         schema_part = full_response.split("---SCHEMA---")[1].split("---REQUEST---")[0].strip()
    #         request_part = full_response.split("---REQUEST---")[1].split("---SOLUTION---")[0].strip()
    #         solution_part = full_response.split("---SOLUTION---")[1].strip()
    #     except IndexError:
    #         raise ValueError("La risposta dell'AI non ha il formato atteso con i separatori. Risposta ricevuta:\n" + full_response)

    #     #return element
    #     return cls(
    #         schema=schema_part,
    #         request=request_part,
    #         solution=solution_part
    #     )