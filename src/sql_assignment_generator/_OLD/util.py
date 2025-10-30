import re

def extract_sql(text: str) -> str:
    match = re.search(r"```sql(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None


def strip_lines(input_str: str) -> str:
    '''
    Strips leading and trailing whitespace from each line of a given string.
    Removes the first and last lines if they are empty.

    Args:
        input_str (str): The input multi-line string.

    Returns:
        str: The processed string with stripped lines.
    '''
    
    lines = input_str.splitlines()

    # Remove leading and trailing empty lines
    if lines and not lines[0].strip():
        lines.pop(0)
    if lines and not lines[-1].strip():
        lines.pop()
    
    # Strip each remaining line
    return '\n'.join(line.strip() for line in lines)
