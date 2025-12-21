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

def execute_query(client, query: str, database: str, table: str):
    """
    Esegue una query su una tabella del database
    """
    result = client.query(query)
    return result



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
        base_url=os.getenv("LLM_BASE_URL"),
        api_key=os.getenv("LLM_API_KEY")
    )

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=messages,
        temperature=temperature
    )

    return response.choices[0].message.content.strip()