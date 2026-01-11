import json
import requests
from state import GraphState
from utils import call_llm, get_table_metadata
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.auth import Auth
from weaviate.classes.query import Filter
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")


def semantic_search(state: GraphState) -> GraphState:

    user_question = state["user_question"]

    # Connessione a Weaviate con context manager
    with weaviate.connect_to_custom(
        http_host=os.getenv("HTTP_HOST_WEAVIATE"),
        http_port=int(os.getenv("HTTP_PORT_WEAVIATE")),
        http_secure=False,
        grpc_host=os.getenv("GRPC_HOST_WEAVIATE"),
        grpc_port=int(os.getenv("GRPC_PORT_WEAVIATE")),
        grpc_secure=False,
        auth_credentials=Auth.api_key(os.getenv("API_KEY_WEAVIATE")),
    ) as client:
        print("Weaviate ready:", client.is_ready())

        # Recupero della collezione
        collection = client.collections.get(os.getenv("COLLECTION_NAME_WEAVIATE"))


        messages = [
            {
                "role": "system",
                "content": """
        Sei un assistente specializzato nello scrivere sinonimi di prodotti, categorie o cose che vengono venduti nei supermercati.
        Identifica nella frase prodotti, categorie di cose, o cose che vengono venduti nei supermercati.
        Stai attento a includere anche a evantuali numeri o quantità correlate con un prodotto specifico (perchè sono distintive del prodotto)
        Se ad esempio la domanda è 'Quali sono i fornitori di lavatrici ?' allora l'entità da individuare è lavatrice.
        Per ogni elemento identificato genera da 2 fino ad un massimo di 4 sinonimi. Non puoi generarne più di 4.
        Scrivi sia i nomi originali che i sinonimi, senza però aggiungere spiegazioni o testo aggiuntivo.
        I sinonimi devono essere diversi dai nomi originali.
        La risposta deve essere su una sola riga. Devi specificare i sinonimi uno dopo l'altro separati da virgola.
        Se la domanda non contiene prodotti, categorie di cose o prodotti, alimenti, e in generale cose trovabili nei supermercati allora devi rispondere con una stringa vuota "".
        Non inventare prodotti non presenti nella domanda.
        """,
            },
            {"role": "user", "content": user_question},
        ]

        sinonimi = call_llm(messages, 0)
        print("sinonimi = ", sinonimi)
       
        client.connect()
        filters = Filter.all_of(
            [
                Filter.by_property("descr_prod").not_equal(
                    "Prodotto non in anagrafica"
                ),
                Filter.by_property("descr_liv1").not_equal(
                    "Categoria non in anagrafica"
                ),
            ]
        )
        
        if len(sinonimi) > 2:
           testo = f"{sinonimi}. {user_question}"
        else:
            testo = f"{user_question}"

        payload = {"model": os.getenv("EMBEDDING_MODEL_NAME"), "prompt": testo}
        res = requests.post(os.getenv("EMBEDDING_MODEL_URL"), json=payload)
        query_vector = res.json()["embedding"]
       
        results = collection.query.hybrid(
            query=testo,
            alpha=0.3,
            limit=4,
            vector=query_vector,
            return_metadata=["score"],
            filters=filters,
        )

        for obj in results.objects:
            item = {
                "cod_prod": obj.properties.get("cod_prod"),
                "descr_prod": obj.properties.get("descr_prod"),
                "descr_liv1": obj.properties.get("descr_liv1"),
                "descr_liv2": obj.properties.get("descr_liv2"),
                "descr_liv3": obj.properties.get("descr_liv3"),
                "descr_liv4": obj.properties.get("descr_liv4"),
                "score": obj.metadata.score,
            }
            state["relevant_items"].append(item)
            
        client.close()
        return state
