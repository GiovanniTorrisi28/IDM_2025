from graph import build_graph
from state import GraphState
import pandas as pd

initial_state: GraphState = {
    "user_question": "Quanti fornitori di birra da 33 cl ci sono nella tabella dei dati di vendita ?",
    "table_schema": None,
    "sql_query": None,
    "query_result": None,
    "query_error": None,
    "retry_count": 0,
    "final_comment": None,
    "is_relevant": None,
    "relevant_items": []
}

app = build_graph()
final_state = app.invoke(initial_state)


# 4️⃣ stampa lo stato corrente per verificare
print("######################\nStato alla fine:")
for k, v in final_state.items():
    print(f"{k}: {v}")
