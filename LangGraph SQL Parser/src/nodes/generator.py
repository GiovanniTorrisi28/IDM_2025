from state import GraphState
from utils import  call_llm

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
    Il nome del mio database è 'eVision' e il nome della mia unica tabella è 'sales_data'.
    Genera una query SQL compatibile con ClickHouse per rispondere alla richiesta dell'utente.
    Richiesta utente: {user_question}
    Schema tabella: {table_schema}
    Restituisci solo la query SQL valida senza aggiungere nessun altro commento.
    """

    if query_error is not None:
        prompt += f"""
        La query SQL che hai generato in precedenza era:
        {previous_query}
        Questa query ha generato il seguente errore:
        {query_error}
        Correggi la query SQL tenendo conto dell'errore.
        Restituisci SOLO la query SQL corretta.
        """

    messages = [
        {"role": "system", "content": "Sei un assistente esperto nel generare query SQL compatibili con ClickHouse."},
        {"role": "user", "content": prompt}
    ]
    
    # chiamata all'llm
    sql_query = call_llm(messages)
    # sql_query = "SELECT COUNT(*) FROM eVision.sales_data0 WHERE anno = 2023"
    return {
        "sql_query": sql_query,
    }
