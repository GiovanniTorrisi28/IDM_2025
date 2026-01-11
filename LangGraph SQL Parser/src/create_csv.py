import clickhouse_connect
import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path

# Carica il .env dalla root del progetto
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# connessione al client clickhouse
client = clickhouse_connect.get_client(
 host = os.getenv("CLICKHOUSE_HOST"),
 port = os.getenv("CLICKHOUSE_PORT"),
 secure = True,
 username = os.getenv("CLICKHOUSE_USER"),
 password = os.getenv("CLICKHOUSE_PASSWORD")
)

# query per raccogliere i dati
result = client.query(
    'SELECT DISTINCT(cod_prod),descr_prod, descr_liv1, descr_liv2, descr_liv3, descr_liv4 FROM "eVision"."sales_data"'
)
df = pd.DataFrame(result.result_rows, columns=result.column_names)

# processing del campo 'descr_prod' per eliminare il codice iniziale e gli spazi successivi
df["descr_prod"] = df["descr_prod"].str.split(n=1).str[1]
df["descr_prod"] = df["descr_prod"].str.rstrip()

# crea il csv specificando il separatore ; e con quoting specifica di non racchiudere nessun valore tra virgolette
df.to_csv("collection_prodotti.csv", index=False, sep=';', quoting=3)
print("lunghezza df = ",len(df))

