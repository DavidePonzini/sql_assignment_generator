
from pydantic import BaseModel
from typing import List
import html


class AssignmentFormat(BaseModel):
    schemas: List[str]
    request: str
    solution: str

    def __str__(self) -> str:
        # request_html = html.escape(self.request).replace('\n', '<br>')
        # solution_html = html.escape(self.solution).replace('\n', '<br>')

        # schema_full_string = "\n".join(self.schemas)
        # schema_html = f'<pre><code>{html.escape(schema_full_string)}</code></pre>'

        # return f'''
        #     <h3>Schema</h3>
        #     <div>{schema_html}</div>
        #     <br>
        #     <h3>Request</h3>
        #     <div>{request_html}</div>
        #     <br>
        #     <h3>Solution</h3>
        #     <div>{solution_html}</div>
        # '''

        return f''' 
SCHEMA
{"\n".join(f"- {item}" for item in self.schemas)}

REQUEST
{self.request}

SOLUTION
{self.solution}
        '''
