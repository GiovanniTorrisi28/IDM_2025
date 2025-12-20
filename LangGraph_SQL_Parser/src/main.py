from nodes.load_user_question import load_user_question
from nodes.load_schema import load_schema
from nodes.generator import generator
from nodes.executor import executor
from state import GraphState

state: GraphState = {
    "user_question": None,
    "table_schema": None,
    "sql_query": None,
    "query_result": None,
    "query_error": None
}

# 1️⃣ inserisci domanda utente
state.update(load_user_question(state, "Quanti prodotti sono stati venduti nell'anno 2023 ?"))

# 2️⃣ carica schema
state.update(load_schema(state))

# 3️⃣ genera SQL con LLM
state.update(generator(state))

# esegue query 
state.update(executor(state))

# 4️⃣ stampa lo stato corrente per verificare
print("Stato dopo A1:")
for k, v in state.items():
    print(f"{k}: {v}")
