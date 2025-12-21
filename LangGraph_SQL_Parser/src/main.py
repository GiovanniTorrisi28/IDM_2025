from graph import build_graph
from state import GraphState

initial_state: GraphState = {
    "user_question": "Quanti prodotti sono stati venduti nell'anno 2023 ?",
    "table_schema": None,
    "sql_query": None,
    "query_result": None,
    "query_error": None,
    "retry_count": 0,
    "_next_node": None
}

app = build_graph()
final_state = app.invoke(initial_state)

# 4️⃣ stampa lo stato corrente per verificare
print("Stato alla fine:")
for k, v in final_state.items():
    print(f"{k}: {v}")


print("\n=== RISULTATO FINALE ===")

if final_state["query_error"] is None:
    print("✅ Query eseguita correttamente")
    for row in final_state["query_result"]:
        print(row)
else:
    print(f"❌ Errore dopo {final_state['retry_count']} tentativi")
    print(final_state["query_error"])


