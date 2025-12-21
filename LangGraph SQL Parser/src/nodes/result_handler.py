from state import GraphState
import pandas as pd

def result_handler(state: GraphState) -> GraphState:
    """
    Gestisce il risultato restituito dall'agente executor
    """
    
    if state['query_error'] is None:
        # query ok: formatta il risultato per essere visualizzato
        result = state['query_result']
        columns = result.column_names
        state["query_result"] = [dict(zip(columns, r)) for r in result.result_rows]
        
        return state
    else:
        # query errata: tiene traccia del numero di errori
        state['retry_count'] += 1
        print("handler, count =",state['retry_count'])
        return state
    