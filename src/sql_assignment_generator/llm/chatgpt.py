from openai import OpenAI
from pydantic import BaseModel
from .message import Message

from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def generate_answer(message: Message, *, json_format: type[BaseModel], add_to_messages: bool = True, **kwargs) -> BaseModel:
    '''
    Generate an answer from the LLM using the provided message and tools.
    '''

    schema = json_format.model_json_schema()
    schema['additionalProperties'] = False      # Required for strict validation

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=message.messages,
        response_format={
            'type': 'json_schema',
            'json_schema': {
                'name': 'Response',
                'strict': True,
                'schema': schema,
            },
        },
        **kwargs
    )

    msg = response.choices[0].message

    if add_to_messages:
        message.add_message_assistant(msg.content)

    return json_format.model_validate_json(msg.content)
        