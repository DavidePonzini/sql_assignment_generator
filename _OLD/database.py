from datetime import datetime

from dav_tools import database, messages, chatgpt


db = database.PostgreSQL(
    database='postgres',
    host='127.0.0.1',
    user='sql_misconceptions_admin',
    password='sql'
)

schema_prefix = 'sql_misconceptions'


def setup_schema(create_tables: str) -> str:
        '''Create a unique schema with the specified tables and return its name'''
        now = datetime.now()
        schema = f'{schema_prefix}_{now.strftime("%Y%m%d%H%M%S%f")}'

        with db.connect() as c:
            c.create_schema(schema)
            # messages.info(f'Created schema "{schema}"')
            c.set_schema(schema)
            c.execute(create_tables)
            # messages.info('Created tables')
            
            c.commit()

        return schema

def delete_schema(schema: str):
    with db.connect() as c:
        c.delete_schema(schema)
        # messages.info(f'Deleted schema "{schema}"')
        
        c.commit()

def create_values(schema: str) -> str:
    message = chatgpt.Message()

    msg = f'''
        Generate at least 20 values for this table and return the result as a INSERT INTO.
        Return only the code as plain text and nothing else.

        {schema}
        '''
    
    message.add_message(chatgpt.MessageRole.USER, msg)
    return message.generate_answer()



def run_queries(schema: str, q1: str, q2: str):
    schema_id = setup_schema(schema)

    try:
         with db.connect() as c:
            c.set_schema(schema_id)
            c.execute(create_values(schema))

            messages.warning('Q1')
            result = c.fetch_all(q1)
            messages.message(result)

            messages.warning('Q2')
            result = c.fetch_all(q2)
            messages.message(result)

    finally:
         delete_schema(schema_id)


if __name__ == '__main__':
    import sys

    create = ''
    print('CREATE')
    for line in sys.stdin:
        create += line

    q1 = ''
    print('Q1')
    for line in sys.stdin:
        q1 += line

    q2 = ''
    print('Q2')
    for line in sys.stdin:
        q1 += line

    run_queries(create, q1, q2)