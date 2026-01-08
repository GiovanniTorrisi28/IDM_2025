import time
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import weaviate
from weaviate.auth import Auth
from weaviate.classes.config import Configure
from weaviate.collections.classes.data import DataObject
from dotenv import load_dotenv
import os
from pathlib import Path

# --------------- CONFIG ---------------

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL_NAME")
OLLAMA_URL = os.getenv("EMBEDDING_MODEL_URL")

BATCH_SIZE = 300
NUM_WORKERS = 10   

CSV_PATH = "collection_prodotti.csv"
COLLECTION_NAME = "MyCollection" # una volta creata la collezione, assegnare questo nome alla variabile COLLECTION_NAME_WEAVIATE

WEAVIATE_HOST = os.getenv("HTTP_HOST_WEAVIATE")
WEAVIATE_HTTP_PORT = os.getenv("HTTP_PORT_WEAVIATE")
WEAVIATE_GRPC_PORT = os.getenv("GRPC_PORT_WEAVIATE")
WEAVIATE_API_KEY = os.getenv("API_KEY_WEAVIATE")

# --------------- EMBEDDING ---------------

def embed(text: str):
    payload = {
        "model": EMBED_MODEL,
        "prompt": text
    }
    res = requests.post(OLLAMA_URL, json=payload)
    res.raise_for_status()
    return res.json()["embedding"]

def build_embedding_text(obj: dict) -> str:
    """
    Costruisce il testo da usare per l'embedding combinando più campi informativi.
    Specificare qui i campi su cui si vuole calcolare l'embedding.
    """
    campi = [
        obj.get("descr_prod", ""),
        obj.get("descr_liv1", ""),
        obj.get("descr_liv2", ""),
        obj.get("descr_liv3", ""),
        obj.get("descr_liv4", "")
    ]

    # Rimuove campi vuoti / None, tiene solo stringhe
    parts = [c for c in campi if c and isinstance(c, str)]

    # Se non c'è nulla, evita di mandare stringa vuota
    if not parts:
        return obj.get("descr_prod", "") or ""

    return ", ".join(parts)


# --------------- MAIN PIPELINE ---------------

with weaviate.connect_to_custom(
   http_host=WEAVIATE_HOST,
   http_port=WEAVIATE_HTTP_PORT,
   http_secure=False,
   grpc_host=WEAVIATE_HOST,
   grpc_port=WEAVIATE_GRPC_PORT,
   grpc_secure=False,
   auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
) as client:

    print("Weaviate ready:", client.is_ready())

    # Ricrei la collection da zero
    client.collections.delete(COLLECTION_NAME)

    if not client.collections.exists(COLLECTION_NAME):
        print(f"Creating collection {COLLECTION_NAME}...")
        client.collections.create(
            name=COLLECTION_NAME,
            vectorizer_config=None 
        )
    else:
        print(f"Collection {COLLECTION_NAME} already exists")

    collection = client.collections.get(COLLECTION_NAME)

    # Carico i dati
    print("Loading CSV...")
    df = pd.read_csv(CSV_PATH, sep=";")

    # Trasforma i dati in un dizionario. Qui si specificano i campi degli oggetti della collezione
    columns_objects = df[[
        "cod_prod",
        "descr_prod",
        "descr_liv1",
        "descr_liv2",
        "descr_liv3",
        "descr_liv4",
    ]].to_dict(orient="records")

    total_start = time.time()

    for i in range(0, len(columns_objects), BATCH_SIZE):
        chunk = columns_objects[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        print(f"\n=== Batch {batch_num} ({len(chunk)} oggetti) ===")

        # Preparazione dei testi per l'embedding 
        t0 = time.time()
        testi = [build_embedding_text(obj) for obj in chunk]
        prep_time = time.time() - t0
        print(f"Tempo preparazione testi: {prep_time:.3f} s")

        # Generazione embedding in parallelo
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            vettori = list(executor.map(embed, testi))
        embed_time = time.time() - t0
        print(f"Tempo embedding (parallel, {NUM_WORKERS} workers): {embed_time:.3f} s")

        # Costruzione oggetto da inserire su weaviate
        t0 = time.time()
        objects_with_vectors = [
            DataObject(
                properties=obj,
                vector=vettore
            )
            for obj, vettore in zip(chunk, vettori)
        ]
        build_obj_time = time.time() - t0
        print(f"Tempo costruzione DataObject: {build_obj_time:.3f} s")

        # Inserimento del batch in weaviate
        t0 = time.time()
        collection.data.insert_many(objects_with_vectors)
        insert_time = time.time() - t0
        print(f"Tempo insert_many: {insert_time:.3f} s")

    total_time = time.time() - total_start
    print(f"\nTempo totale import: {total_time:.3f} s")