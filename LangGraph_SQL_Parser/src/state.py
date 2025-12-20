from typing import TypedDict, Optional, Dict

class GraphState(TypedDict):
    user_question: Optional[str]
    table_schema: Optional[Dict[str, str]]
    sql_query: Optional[str]
    is_success: Optional[bool]
    query_result: Optional[dict]
