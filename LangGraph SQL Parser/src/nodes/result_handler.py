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
        print("query ok\n",pd.DataFrame(state['query_result']))
        
        return state
    else:
        # query errata
        print("la query non si può fare, count = ",state['retry_count'])
        return state
    