# nodes/load_schema.py
from state import GraphState
from utils import get_clickhouse_client, get_table_schema


def load_schema(state: GraphState) -> dict:
    """
    Interroga il database remoto ClickHouse per ottenere lo schema della tabella 'sales_data'
    """
    client = get_clickhouse_client()
    schema = get_table_schema(client, "eVision", "sales_data")
    return {"table_schema": schema}
