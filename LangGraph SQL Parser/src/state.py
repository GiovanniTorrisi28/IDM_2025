from typing import TypedDict, Optional, Dict

class GraphState(TypedDict):
    user_question: Optional[str]
    table_schema: Optional[Dict[str, str]]
    sql_query: Optional[str]
    query_error: Optional[str]
    query_result: Optional[any]#Optional[list[dict]]
    retry_count: int
    final_response: Optional[str]