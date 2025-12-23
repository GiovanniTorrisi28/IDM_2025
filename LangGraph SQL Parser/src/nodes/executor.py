from state import GraphState
from utils import get_clickhouse_client

def executor(state: GraphState) -> GraphState:
    """
    Eseguire la query generata dall'agente 'generator' sul database ClickHouse e restituire il risultato
    """
    query = state["sql_query"]
    client = get_clickhouse_client()

    try:
        # query corretta
        result = client.query(query)
        state["query_error"] = None
        state["query_result"] = result
        return state
    
    except Exception as e:
        # query con errori di sintassi
        state["query_result"] = None
        state["query_error"] = str(e)
        state['retry_count'] += 1
        return state
    