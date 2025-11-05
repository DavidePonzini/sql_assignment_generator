from pydantic import BaseModel, ValidationError
from dav_tools import chatgpt
from typing import List


class SchemaResponse(BaseModel):
    """Modello per la risposta JSON contenente lo schema SQL."""
    schema: List[str]

class RequestResponse(BaseModel):
    """Modello per la risposta JSON contenente la richiesta in linguaggio naturale."""
    request: str

class SolutionResponse(BaseModel):
    """Modello per la risposta JSON contenente la query di soluzione."""
    solution: str


def _generate_json_part(base_context: str, instruction: str, response_model: BaseModel) -> str | List[str]:
    """
    Metodo di supporto per eseguire una singola chiamata all'AI che deve restituire JSON.
    Pulisce la risposta da eventuali blocchi di codice Markdown.
    """
    chat = chatgpt.Message()
    full_instruction = (
        f"Basandoti su questo concetto di esercizio:\n---\n{base_context}\n---\n"
        f"{instruction}\n"
        "La tua intera risposta, dal primo all'ultimo carattere, DEVE essere un oggetto JSON valido."
    )
    chat.add_message(chatgpt.MessageRole.USER, full_instruction)
    
    json_response_str = chat.generate_answer(
        model=chatgpt.AIModel.GPT4o_mini
    )

    if json_response_str is None:
        raise RuntimeError("La funzione generate_answer ha restituito None.")

    # --- INIZIO MODIFICA CHIAVE: Pulizia della stringa ---
    # Rimuove i blocchi di codice Markdown e altri spazi bianchi.
    if "```json" in json_response_str:
        # Estrae il contenuto tra il primo '{' e l'ultimo '}'
        start = json_response_str.find('{')
        end = json_response_str.rfind('}')
        if start != -1 and end != -1:
            json_response_str = json_response_str[start:end+1]
    # --- FINE MODIFICA CHIAVE ---

    try:
        validated_response = response_model.model_validate_json(json_response_str)
        # Restituisce il valore del primo (e unico) campo del modello.
        # Ora può essere una stringa o una lista.
        return list(validated_response.model_dump().values())[0]
    except ValidationError as e:
        raise ValueError(f"La risposta JSON dell'AI non è valida.\nErrore: {e}\nRisposta ricevuta:\n{json_response_str}")
    except Exception as e:
        raise RuntimeError(f"Errore imprevisto durante il parsing della risposta JSON: {e}")