# nodes/load_user_question.py
from state import GraphState
from utils import call_llm, get_table_metadata
import json

def load_user_question(state: GraphState) -> dict:
    
    user_question = state["user_question"]
    messages=[
        {"role": "system", "content": f"""Sei un agente di classificazione.
       Il tuo compito è determinare se una richiesta utente rientra nell'ambito
       di un sistema che risponde a domande utilizzando un database di
       ricevute di supermercati e prodotti venduti.
       Devi SOLO classificare la richiesta e restituire true o false e una brevissima spiegazione del perchè della tua decisione. 
       Restituisci questi dati in formato json con i campi is_relevant e explanation. Restituisci solo il json senza nessun altro commento o simbolo perchè deserializzerò direttamente la tua risposta.
       Ecco l'elenco delle colonne della tabella di riferimento con il relativo significato: {get_table_metadata()}
    Per rispondere devi comprendere alla perfezione la richiesta dell'utente poi rispondere true se con i dati a disposizione sapresti costruire una query sql che risponde alla domanda dell'utente, o restituire false altrimenti.
          """},
        {"role": "user", "content": f"""Classifica la seguente richiesta: {user_question}"""}
    ]

    response = call_llm(messages, 0.1) 
    data = json.loads(response)
    state["is_relevant"] = data["is_relevant"]
    state["final_comment"] = data["explanation"]
    print("filtro = ",state["is_relevant"])
    return state
