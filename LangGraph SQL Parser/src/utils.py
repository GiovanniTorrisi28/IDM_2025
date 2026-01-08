import clickhouse_connect
from dotenv import load_dotenv
import os
from pathlib import Path
from openai import OpenAI


def get_table_schema(client, database: str, table: str):
    """
    Restituisce uno schema della tabella come dict {colonna: tipo}
    """
    query = f'DESCRIBE TABLE "{database}"."{table}"'
    result = client.query(query)
    schema = {row[0]: row[1] for row in result.result_rows}
    return schema


# Carica il .env dalla root del progetto
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


def get_clickhouse_client():
    """
    Funzione che restituisce un client ClickHouse
    """

    host = os.getenv("CLICKHOUSE_HOST")
    port = int(os.getenv("CLICKHOUSE_PORT"))
    user = os.getenv("CLICKHOUSE_USER")
    password = os.getenv("CLICKHOUSE_PASSWORD")
    database = os.getenv("CLICKHOUSE_DATABASE")

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        # database=database
    )

    return client


def call_llm(messages, temperature: float = 0.2) -> str:
    """
    Funzione che chiama l'LLM e restituisce solo il contenuto testuale della risposta.
    """

    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL"), api_key=os.getenv("LLM_API_KEY")
    )

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"), messages=messages, temperature=temperature
    )

    return response.choices[0].message.content.strip()


def get_table_metadata():
    """
    Funzione che definisce e restituisce una struttura dati dizionario
    che contiene il nome delle colonne e il loro significato semantico.
    """

    table_metadata = {
        "nome_tabella": "sales_data",
        "colonne": {
            "id_sc": "Identificativo univoco dello scontrino; identifica una singola transazione di acquisto",
            "pv": "Identificativo del punto vendita (supermercato) in cui è avvenuta la vendita",
            "anno": "Anno solare in cui è stato acquistato il prodotto (derivato dalla data dello scontrino)",
            "data": "Data completa dello scontrino nel formato anno-mese-giorno (YYYY-MM-DD)",
            "cassa": "Identificativo della cassa del supermercato su cui è stato effettuato il pagamento",
            "cassiere": "Identificativo del dipendente (cassiere) che ha gestito la transazione",
            "num_scontrino": "Numero progressivo dello scontrino all’interno del punto vendita",
            "ora": "Orario in cui è stato effettuato l’acquisto (HH:MM o HH:MM:SS)",
            "tessera": "Identificativo della tessera fedeltà del cliente, se utilizzata durante l’acquisto",
            "t_flag": "Codice che indica il tipo di operazione della riga di vendita (es. vendita normale, reso, annullamento)",
            "num_riga": "Numero progressivo della riga all’interno dello scontrino",
            "r_reparto_cdaplus": "Codice del reparto merceologico associato alla riga di vendita secondo la codifica CDAPLUS",
            "r_qta_pezzi": "Quantità di pezzi acquistati per il prodotto nella specifica riga dello scontrino",
            "r_peso": "Peso totale del prodotto acquistato nella riga (usato per prodotti venduti a peso)",
            "r_importo_lordo": "Importo lordo totale della riga di vendita, comprensivo di imposte",
            "r_imponibile": "Importo imponibile della riga di vendita, esclusa l’IVA",
            "r_iva": "Aliquota IVA applicata alla riga di vendita (in percentuale)",
            "r_sconto": "Importo totale dello sconto applicato alla riga di vendita",
            "r_sconto_fide": "Importo dello sconto applicato tramite programmi di fidelizzazione (tessera fedeltà)",
            "r_sconto_rip": "Quota di sconto ripartita sulla riga (ad esempio sconti distribuiti su più prodotti)",
            "r_tipo_riga": "Tipologia della riga di scontrino (es. normale, annullo, reso)",
            "cod_prod": "Codice identificativo univoco del prodotto acquistato",
            "descr_prod": "Descrizione testuale del prodotto; contiene il codice prodotto seguito dal nome o descrizione commerciale",
            "cod_forn": "Codice identificativo del fornitore del prodotto",
            "descr_forn": "Nome o descrizione del fornitore del prodotto",
            "descr_liv1": "Descrizione testuale della categoria merceologica di livello 1 del prodotto",
            "liv1": "Codice numerico della categoria merceologica di livello 1 del prodotto",
            "descr_liv2": "Descrizione testuale della categoria merceologica di livello 2 del prodotto",
            "liv2": "Codice numerico della categoria merceologica di livello 2 del prodotto",
            "descr_liv3": "Descrizione testuale della categoria merceologica di livello 3 del prodotto",
            "liv3": "Codice numerico della categoria merceologica di livello 3 del prodotto",
            "descr_liv4": "Descrizione testuale della categoria merceologica di livello 4 del prodotto",
            "liv4": "Codice numerico della categoria merceologica di livello 4 del prodotto",
            "tipologia": "Codice che identifica la tipologia commerciale del prodotto",
            "descr_tipologia": "Descrizione testuale della tipologia commerciale del prodotto",
            "cod_rep": "Codice del reparto del supermercato in cui è collocato il prodotto",
            "descr_rep": "Descrizione testuale del reparto del supermercato",
            "rag_sociale": "Identificativo della filiale o ragione sociale del punto vendita (coincidente con il punto vendita)",
            "localita": "Città in cui si trova il supermercato",
            "provincia": "Provincia in cui si trova il supermercato",
        },
        "info per la scelta delle colonne nelle query": "i campi liv e cod contengono codici numeri come ad esempio 0987, mentre i corrispondenti campi descr sono adatti a fare ricerce su parole del linguaggio naturale",
    }

    return table_metadata
