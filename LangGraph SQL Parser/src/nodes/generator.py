from state import GraphState
from utils import call_llm, get_table_metadata


def generator(state: GraphState) -> GraphState:
    user_question = state["user_question"]
    table_schema = state["table_schema"]
    query_error = state["query_error"]
    previous_query = state["sql_query"]
    print("Generatore: ", user_question)
    messages = [
        {
            "role": "system",
            "content": f"""Sei un assistente esperto nel generare query SQL compatibili con ClickHouse. A partire dalla richiesta dell'utente devi restituire in output solo la query senza aggiungere nessun commento o simbolo extra come ad esempio i tre apici
            di inizio e fine stringa ``` o altro che sia diverso dal codice sql perchè io prenderò la tua risposta e la eseguirò direttamente.
            Il database si chiama eVision e la tabella si chiama sales_data.
            La tabella contiene dati di vendita di vari supermercati, in particolare ogni riga corrisponde ad un prodotto scansionato alla cassa.
            Lo schema della tabella di riferimento è {table_schema} e a seguire ecco una spiegazione del significato delle colonne: {get_table_metadata()}.
            Le colonne di tipo stringa hanno valori esclusivamente scritti in maiuscolo, tieni conto di questa forma quando formuli la query.
            Usa di default la direttiva sql LIMIT 100 a meno che l'utente non specifichi che vuole un certo numero di risultati.
            Genera solo query SELECT.
            Cerca di rendere la risposta quanto più leggibile possibile nei nomi e nel formato dei valori delle colonne.
            questi sono esempi di oggetti correlati con la richiesta utente. 
            puoi usare questi oggetti per individuare le colonne e i valori migliori per fare una query quanto più giusta possibile
            (ad esempio se vedi che i valori con score piu alto hanno dei valori uguali in certe colonne allora usa questa informazione).
            {state['relevant_items']}

            """,
        },
        {"role": "user", "content": f"{user_question}"},
    ]
    

    if query_error is not None:
        messages.extend(
            [
                {"role": "assistant", "content": previous_query},
                {
                    "role": "system",
                    "content": f"""
                        La query precedente ha causato il seguente errore SQL:
                        {query_error}

                        Correggi la query mantenendo lo stesso obiettivo.
                        """,
                },
            ]
        )

    sql_query = call_llm(messages,0)

    print("query generata =", sql_query)
    return {"sql_query": sql_query}
