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
    Chiama l'LLM e restituisce solo il contenuto testuale della risposta.
    """

    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL"), api_key=os.getenv("LLM_API_KEY")
    )

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"), messages=messages, temperature=temperature
    )

    return response.choices[0].message.content.strip()


def get_table_metadata():
    table_metadata = {
        "nome_tabella": "sales_data",
        "colonne": {
            "id_sc": "id dello scontrino",
            "pv": "id del supermercato",
            "anno": "anno in cui è stato acquistato il prodotto",
            "data": "data dello scontrino nel formato anno-mese-giorno",
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
            "descr_prod": "questo campo è diviso in due parti: prima si ripete il codice del prodotto e poi c'è la descrizione del prodotto acquistato",
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
            "provincia": "provincia in cui si trova il supermercato",
        },
    }
    return table_metadata


def format_metadata(dizionario):
    riga = []
    for colonna, spiegazione in dizionario.items():
        riga.append(f"- {colonna}: {spiegazione}")
    return "\n".join(riga)
