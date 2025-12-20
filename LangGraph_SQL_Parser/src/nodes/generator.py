from state import GraphState
from utils import  call_llm

def generator(state: GraphState) -> GraphState:
    """
    Legge la domanda dell'utente e genera una query SQL compatibile con ClickHouse.
    Usa lo schema della tabella per guidare la query.
    """
    user_question = state["user_question"]
    table_schema = state["table_schema"]

    prompt = f"""
    Il nome del mio database è 'eVision' e il nome della mia unica tabella è 'sales_data'.
    Genera una query SQL compatibile con ClickHouse per rispondere alla richiesta dell'utente.
    Richiesta utente: {user_question}
    Schema tabella: {table_schema}
    Restituisci solo la query SQL valida senza aggiungere nessun altro commento.
    """

    messages = [
        {"role": "system", "content": "Sei un assistente esperto nel generare query SQL compatibili con ClickHouse. Quando fai una query devi specificare nella clausola FROM il nome del database e il nome della tabella"},
        {"role": "user", "content": prompt}
    ]
    
    # chiamata all'llm
    #sql_query = call_llm(messages)
   
    return {
        "sql_query": "SELECT COUNT(*) FROM eVision.sales_data WHERE anno = 2024"
    }
