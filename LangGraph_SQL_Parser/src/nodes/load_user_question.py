# nodes/load_user_question.py
from state import GraphState

def load_user_question(state: GraphState, question: str) -> dict:
    return {"user_question": question}
