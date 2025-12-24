from state import GraphState
from utils import call_llm, format_metadata, get_table_metadata


def generator(state: GraphState) -> GraphState:
    """
    Legge la domanda dell'utente e genera una query SQL compatibile con ClickHouse.
    Usa lo schema della tabella per guidare la query.
    """

    user_question = state["user_question"]
    table_schema = state["table_schema"]
    query_error = state["query_error"]
    previous_query = state["sql_query"]

    prompt = f"""
       Richiesta utente: {user_question}
       Restituisci solo la query SQL valida senza aggiungere nessun altro commento.
       """

    if query_error is not None:
        prompt += f"""
            La query SQL che hai generato in precedenza era:
            {previous_query}
            Questa query ha generato il seguente errore:
            {query_error}
            Correggi la query SQL tenendo conto dell'errore.
            """

    sql_query = call_llm(get_query_messages(prompt, table_schema))
    # sql_query = """SELECT pv, SUM(r_importo_lordo) AS incassi FROM eVision.sales_data WHERE anno = 2024 GROUP BY pv ORDER BY incassi DESC LIMIT 1"""
    print("query generata = ",sql_query)
    return {
        "sql_query": sql_query,
    }


def get_query_messages(prompt, table_schema):
    messages = [
        {
            "role": "system",
            "content": f"""Sei un assistente esperto nel generare query SQL compatibili con ClickHouse.
            A partire dalla richiesta dell'utente devi restituire in output solo la query senza aggiungere nessun commento o simbolo extra come ad esempio i tre apici ``` di inizio e fine string o altro che sia diverso dal codice sql perchè io prenderò la tua risposta e la eseguirò direttamente.
            Il database si chiama eVision e la tabella si chiama sales_data.
            La tabella contiene dati di vendita di vari supermercati, in particolare ogni riga corrisponde ad un prodotto scansionato alla cassa.
            Lo schema della tabella di riferimento è {table_schema} e a seguire ecco una spiegazione del significato delle colonne: {get_table_metadata()}.
            Usa di default la direttiva sql LIMIT 500 a meno che l'utente non specifichi che vuole un numero inferiore di risultati.
            """,
        },
        {"role": "user", "content": prompt},
    ]
    return messages
