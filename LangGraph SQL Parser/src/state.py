from typing import TypedDict, Optional, Dict


class GraphState(TypedDict):
    """
    Classe che definisce lo stato dell'automa a stati finiti di LangGraph.
    """

    user_question: Optional[str]
    table_schema: Optional[Dict[str, str]]
    sql_query: Optional[str]
    query_error: Optional[str]
    query_result: Optional[any]  # Optional[list[dict]]
    retry_count: int
    final_comment: Optional[str]
    is_relevant: bool
    relevant_items: list
