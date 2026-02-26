from ...constraints import QueryConstraint
from sqlscope import Query
from ...translatable_text import TranslatableText

def prompt_generate(
        dataset_str: str,
        extra_details: str,
        constraints: list[QueryConstraint],
        *,
        sql_dialect: str,
        language: str
    ) -> str:

    formatted_constraints = '\n'.join(f'- {constraint.description.get(language)}' for constraint in constraints)

    if extra_details.strip():
        extra_details_formatted = TranslatableText(
            f"The exercise must have the following characteristics:\n{extra_details}",
            it=f"L'esercizio deve avere le seguenti caratteristiche:\n{extra_details}"
        ).get(language)
    else:
        extra_details_formatted = ""

    return TranslatableText(
        f'''
### CONTEXT (DATABASE SCHEMA AND DATA) ###
{dataset_str}

### GUIDELINES ###
Generate a {sql_dialect} SQL exercise based on the dataset above.
{extra_details_formatted}

### MANDATORY REQUIREMENTS FOR THE EXERCISE ###
{formatted_constraints}

#### JSON REQUIRED OUTPUT FORMAT ####
{{
    "request": "Extract and return ONLY the natural language query request, following the specified constraints. Never ask to include mistakes. Be concise and clear. Do not provide hints or explanations.",
    "solution": "Only a single syntactically and semantically correct (i.e. executable with minimum 1 returned row) SQL query that solves the exercise."
}}
''',
            it=f'''
### CONTESTO (SCHEMA DEL DATABASE E DATI) ###
{dataset_str}

### LINEE GUIDA ###
Genera un esercizio SQL {sql_dialect} basato sul dataset sopra.
{extra_details_formatted}

### REQUISITI OBBLIGATORI PER L'ESERCIZIO ###
{formatted_constraints}

#### FORMATO DI OUTPUT RICHIESTO IN JSON ####
{{
    "request": "Estrai e restituisci SOLO la richiesta in linguaggio naturale, seguendo i vincoli specificati. Non chiedere mai di includere errori. Sii conciso e chiaro. Non fornire suggerimenti o spiegazioni.",
    "solution": "Solo una singola query SQL sintatticamente e semanticamente corretta (cioè eseguibile con almeno 1 riga restituita) che risolve l'esercizio."
}}
'''
        ).get(language)


def feedback_validation_errors(errors: list[str], *, language: str) -> str:
    return TranslatableText(
        f"The previous JSON output was rejected because it violated these constraints: {', '.join(errors)}\n Regenerate the JSON to satisfy all constraints.",
        it=f"Il precedente output JSON è stato rifiutato perché violava questi vincoli: {', '.join(errors)}\n Rigenera il JSON per soddisfare tutti i vincoli."
    ).get(language)


def prompt_refine_request(request: str, query: Query, *, language: str) -> str:
    result = TranslatableText(
        f'''For the following query solution:
--- SOLUTION START ---
{query.sql}
--- SOLUTION END ---

Reword the natural language request to remove any kind of hints on how to write it. 
Keep the condition purely at the problem level, not the SQL level.
Keep it realistic, simple and straightforward. It doesn't have to sound like a school exercise, but like a real-world request.
Do not use generic phrases like "a certain amount"; instead specify exact terms.
Avoid mentioning tables explicitly. Remove any reference to joins or join keys.
Do not use any formatting on the answer.
''',
        it=f'''Per la seguente soluzione SQL:
--- SOLUTION START ---
{query.sql}
--- SOLUTION END ---

Riformula la richiesta in linguaggio naturale per rimuovere qualsiasi tipo di suggerimento su come scriverla.
Mantieni la condizione puramente a livello di problema, non a livello SQL.
Mantienila realistica, semplice e diretta. Non deve suonare come un esercizio scolastico, ma come una richiesta del mondo reale.
Non usare frasi generiche come "una certa quantità"; specifica invece termini esatti.
Evita di menzionare esplicitamente le tabelle. Rimuovi qualsiasi riferimento a join o chiavi di join.
Non usare alcun formato nella risposta.
'''
    )

    # Aliases
    result += TranslatableText(
        "Make it clear which columns should be selected. If any columns are aliased in the solution, make sure to reflect that in the request, otherwise students might be confused.",
        it="Fai in modo che sia chiaro quali colonne devono essere selezionate. Se alcune colonne sono alias nella soluzione, assicurati di riflettere questo nel request, altrimenti gli studenti potrebbero essere confusi."
    )

    aliases: list[tuple[str, str]] = []
    for col in query.main_query.output.columns:
        if col.name != col.real_name:
            aliases.append((col.real_name, col.name))

    if aliases:
        aliases_str = ', '.join([f'"{alias}"' for real_name, alias in aliases])
        result += TranslatableText(
            f"\nIn particular, you must specify the need to use the following aliases: {aliases_str}.",
            it=f"\nIn particolare, devi specificare la necessità di utilizzare i seguenti alias: {aliases_str}."
        )

    result += TranslatableText(
        f'''

Natural Language Request:
--- REQUEST START ---
{request}
--- REQUEST END ---
''',
        it=f'''

Richiesta in Linguaggio Naturale:
--- REQUEST START ---
{request}
--- REQUEST END ---
'''
    )

    return result.get(language)