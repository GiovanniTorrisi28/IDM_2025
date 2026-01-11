from langgraph.graph import StateGraph, END
from state import GraphState
from nodes.guard import guard
from nodes.load_schema import load_schema
from nodes.generator import generator
from nodes.executor import executor
from routing.choose_if_retry import choose_if_retry
from routing.choose_if_continue import choose_if_continue
from nodes.result_handler import result_handler
from nodes.semantic_search import semantic_search
from nodes.rewriter import rewriter

def build_graph():
    """
    Funzione di costruzione del grafo di LangGraph.
    """

    graph = StateGraph(GraphState, read_next_node=True)

    # dichiarazione die nodi
    graph.add_node("rewriter",rewriter)
    graph.add_node("guard", guard)
    graph.add_node("semantic_search", semantic_search)
    graph.add_node("load_schema", load_schema)
    graph.add_node("generator", generator)
    graph.add_node("executor", executor)
    graph.add_node("result_handler", result_handler)

    # dichiarazione entry point
    graph.set_entry_point("rewriter")
    
    # dichiarazione archi
    graph.add_edge("rewriter","guard")
    graph.add_conditional_edges(
        "guard",  # Nodo sorgente
        choose_if_continue,  # Funzione di instradamento
        {
            "continue": "semantic_search",  # valore restituito : nome prossimo nodo
            "stop": END,  # END è una costante del framework
        },
    )
    graph.add_edge("semantic_search", "load_schema")
    graph.add_edge("load_schema", "generator")
    graph.add_edge("generator", "executor")
    graph.add_conditional_edges(
        "executor",  
        choose_if_retry,  
        {
            "retry": "generator", 
            "continue": "result_handler",
        },
    )

    return graph.compile()
