from typing import Literal
from state import GraphState


def choose_if_continue(state: GraphState) -> Literal["continue", "end"]:
    """
    Funzione di decisione per instradare i dati nel grafo.
    Si decide il percorso tra : guard -> generator o guard -> result_handler
    """

    is_relevant = state["is_relevant"]

    if is_relevant == True:  # la domanda è coerente, si può continuare
        return "continue"
    else:
        return (
            "end"  # la domanda non è coerente, si può terminare e gestire il risultato
        )
