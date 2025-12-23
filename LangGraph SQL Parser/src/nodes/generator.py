from state import GraphState
from utils import  call_llm

def generator(state: GraphState) -> GraphState:
    """
    Legge la domanda dell'utente e genera una query SQL compatibile con ClickHouse.
    Usa lo schema della tabella per guidare la query.
    """
    user_question = state["user_question"]
    table_schema = state["table_schema"]
    query_error = state["query_error"]
    previous_query = state["sql_query"]

    prompt = f"""
    Richiesta utente: {user_question}
    Restituisci solo la query SQL valida senza aggiungere nessun altro commento.
    """

    if query_error is not None:
        prompt += f"""
        La query SQL che hai generato in precedenza era:
        {previous_query}
        Questa query ha generato il seguente errore:
        {query_error}
        Correggi la query SQL tenendo conto dell'errore.
        Restituisci SOLO la query SQL corretta.
        """
    
    table_metadata = format_metadata(table_schema)
    messages = [
        {"role": "system", "content": f"""Sei un assistente esperto nel generare query SQL compatibili con ClickHouse.
            A partire dalla richiesta dell'utente devi restituire in output solo la query senza aggiungere nessun commento o simbolo perchè io prenderò la tua risposta e la eseguirò direttamente.
            Il database si chiama eVisione e la tabella si chiama sales_data.
            La tabella contiene dati di vendita di vari supermercati, in particolare ogni riga corrisponde ad un prodotto scansionato alla cassa.
            Lo schema della tabella di riferimento è {table_schema} e a seguire ecco una spiegazione del significato delle colonne: {table_metadata}.
            """},
        {"role": "user", "content": prompt}
    ]
    
    # chiamata all'llm
    sql_query = call_llm(messages)
    # sql_query = "SELECT COUNT(*) FROM eVision.sales_data WHERE anno = 2023"
    return {
        "sql_query": sql_query,
    }


def get_table_metadata():
    table_metadata = {
        "nome_tabella": "sales_data",
        "colonne": {
            "id_sc" : "id dello scontrino",
            "pv" : "id del supermercato",
            "data" : "data dello scontrino nel formato anno-mese-giorno",
            "cassa": "id della cassa del supermercato",
            "cassiere": "id del dipendente cassiere",
            "num_scontrino": "numero dello scontrino",
            "ora": "orario dell'acquisto",
            "tessera": "id della tessera del supermercato del cliente",
            "t_flag": "",
            "num_riga": "numero della riga",
            "r_reparto_cdaplus": "",
            "r_qta_pezzi": "quantità acquistata di un certo prodotto in una transazione (stesso scontrino, la riga)",
            "r_peso": "peso totale della riga",
            "r_importo_lordo": "prezzo lordo della riga",
            "r_imponibile": "prezzo imponibile della riga( prezzo senza considerare l'Iva o altre imposte)",
            "r_iva": "Percentuale dell'imposta IVA applicata sulla riga",
            "r_sconto": "sconto applicato sulla riga",
            "r_sconto_fide": "sconto applicato sulla riga legato a programmi di fidelity card",
            "r_sconto_rip": "sconto ripartito della riga",
            "r_tipo_riga": "tipo della riga",
            "cod_prod": "codice del prodotto acquistato",
            "descr_prod": "descrizione del prodotto acquistato",
            "cod_forn": "codice del fornitore del prodotto",
            "descr_forn": "descrizione del fornitore del prodotto",
            "liv1": "codice di livello 1 della GDO del prodotto acquistato",
            "descr_liv1": "descrizione relativa al codice del livello 1 del prodotto acquistato",
            "liv2": "codice di livello 2 della GDO del prodotto acquistato",
            "descr_liv2": "descrizione relativa al codice del livello 2 del prodotto acquistato",
            "liv3": "codice di livello 3 della GDO del prodotto acquistato",
            "descr_liv3": "descrizione relativa al codice del livello 3 del prodotto acquistato",
            "liv4": "codice di livello 4 della GDO del prodotto acquistato",
            "descr_liv4": "descrizione relativa al codice del livello 4 del prodotto acquistato",
            "tipologia": "codice relativo alla tipologia del prodotto",
            "descr_tipologia": "descrizione della tipologia del prodotto",
            "cod_rep": "codice del reparto in cui si trova il prodotto",
            "descr_rep": "descrizione del reparto in cui si trova il prodotto",
            "rag_sociale": "identificativo della filiale (dovrebbe coicidere con il campo pv)",
            "localita": "città in cui si trova il supermercato",
            "provincia": "provincia in cui si trova il supermercato"
        }
    }
    return table_metadata
    
def format_metadata(dizionario):
    linee = []
    for colonna, spiegazione in dizionario.items():
        linee.append(f"- {colonna}: {spiegazione}")
    return "\n".join(linee)
