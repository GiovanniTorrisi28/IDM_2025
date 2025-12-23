from graph import build_graph
from state import GraphState
import pandas as pd

initial_state: GraphState = {
    "user_question": "Quanti prodotti sono stati venduti nell'anno 2023 ?",
    "table_schema": None,
    "sql_query": None,
    "query_result": None,
    "query_error": None,
    "retry_count": 0,
    "final_response": None
}

app = build_graph()
final_state = app.invoke(initial_state)

# 4️⃣ stampa lo stato corrente per verificare
print("Stato alla fine:")
for k, v in final_state.items():
    print(f"{k}: {v}")
