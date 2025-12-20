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
        # result_rows è una lista di tuple
        # convertiamo in lista di dizionari colonna->valore
        columns = result.column_names
        rows = [dict(zip(columns, r)) for r in result.result_rows]

        return {"query_result": rows, "query_error": None}

    except Exception as e:
        print(f"[Validator] Errore esecuzione query: {e}")
        return {"query_result": None, "query_error": str(e)}
    