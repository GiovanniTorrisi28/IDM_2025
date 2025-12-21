from typing import Literal
from state import GraphState

def router(state: GraphState) -> Literal["retry", "end"]:
    retry_count = state["retry_count"]

    if state["query_error"] is None:
        return "end"
    elif retry_count < 3:
        return "retry"
    return "end"
