# nodes/load_user_question.py
from state import GraphState


def load_user_question(state: GraphState) -> dict:
    return {
        "user_question": "Quanti prodotti sono stati venduti in ogni mese dell'anno 2023 ? "
    }
