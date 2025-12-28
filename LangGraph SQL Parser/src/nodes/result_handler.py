from state import GraphState
import pandas as pd
from utils import call_llm, get_table_metadata


def result_handler(state: GraphState) -> GraphState:
    """
    Gestisce il risultato restituito dall'agente executor o dall'agente guard.
    """

    result = state["query_result"]
    error = state["query_error"]
    is_relevant = state["is_relevant"]
    
    if is_relevant == False: # la richiesta non è pertinente, si può terminare
        return state
    
    elif error is None:  # query ok
        columns = result.column_names
        state["query_result"] = pd.DataFrame(
            [dict(zip(columns, r)) for r in result.result_rows]
        )
        print("query ok\n", state["query_result"])
        state["final_comment"] = call_llm(get_comment_prompts(state), 0.5)
        print("commento = ",state["final_comment"])

        return state
    else:  # query errata
        print("la query non si può fare, count = ", state["retry_count"])

        state["final_comment"] = call_llm(get_comment_prompts(state), 0.5)
        print("commento =", state["final_comment"])

        return state


def get_comment_prompts(state: GraphState):
    """
    Funzione di supporto che restituisce i prompt di sistema e utente per commentare il risultato della query
    """

    messages = [
        {
            "role": "system",
            "content": f"""Sei un assistente esperto nell'analisi dati. 
            Il tuo compito è commentare i risultati di query SQL in modo chiaro e professionale.
            Usa queste descrizioni delle colonne per interpretare correttamente i dati:
            {get_table_metadata()}
            
            REGOLE:
            - Sii conciso (poche righe).
            - Non essere verboso.
            - Se i dati sono vuoti, segnalalo gentilmente.""",
        },
        {
            "role": "user",
            "content": f"""Commenta il risultato della seguente analisi:
            
            DOMANDA UTENTE: {state["user_question"]}
            QUERY ESEGUITA: {state["sql_query"]}
            RISULTATO OTTENUTO: {state["query_result"]}
            ERRORE OTTENUTO; {state["query_error"]}
            Forniscimi un commento breve.""",
        },
    ]
    return messages
