from typing import Literal
from state import GraphState


def router2(state: GraphState) -> Literal["continue", "end"]:
    is_relevant = state["is_relevant"]

    if is_relevant == True: # la domanda è coerente, si può continuare
       return "continue"
    else :
        return "end" # la domanda non è coerente, si può terminare e gestire il risultato
