from state import GraphState
from utils import call_llm, get_table_metadata


def rewriter(state: GraphState) -> GraphState:
    user_question = state["user_question"]
    messages = [
        {
            "role": "system",
            "content": f"""Sei un assistente esperto nel chiarire l'intento degli input testuali che ricevi.
             Riscrivi la richiesta rendendola più chiara e non ambigua, senza aggiungere informazioni extra.
             Tieni conto che un llm successivo elaborerà la tua risposta per decidere se è coerente o meno con un certo contesto applicativo.
           
            """,
        },
        {"role": "user", "content": f"{user_question}"},
    ]

    user_question_riformulata = call_llm(messages, 0)

    print("Richiesta riformulata =", user_question_riformulata)
    state['user_question'] = user_question_riformulata
    return state