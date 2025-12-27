from typing import Literal
from state import GraphState


def router(state: GraphState) -> Literal["retry", "end"]:
    """
    Funzione di decisione per instradare i dati nel grafo.
    Si decide il percorso tra : executor -> result_handler o executor -> generator
    """

    retry_count = state["retry_count"]

    if state["query_error"] is None:  # nessun errore: si può terminare
        return "end"
    elif retry_count < 3:  # errore: si riprova a rigenerare la query
        return "retry"
    # si è raggiunto il numero massimo di correzioni: si può terminare
    return "end"
