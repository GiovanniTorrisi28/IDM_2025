from state import GraphState
from utils import get_clickhouse_client

def executor(state: GraphState) -> GraphState:
    """
    Eseguire la query generata dall'agente 'generator' sul database ClickHouse e restituire il risultato
    """
    query = state["sql_query"]
    client = get_clickhouse_client()

    try:
        result = client.query(query)
        state["retry_count"] += 1
        # result_rows è una lista di tuple
        # convertiamo in lista di dizionari colonna->valore
        columns = result.column_names
        state["query_result"] = [dict(zip(columns, r)) for r in result.result_rows]
        state["query_error"] = None
        return state
    
    except Exception as e:
        print(f"[Validator] Errore esecuzione query: {e}")
        state["retry_count"] += 1
        state["query_result"] = None
        state["query_error"] = str(e)
        return state
    