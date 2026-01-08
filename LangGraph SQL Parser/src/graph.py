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


def build_graph():
    """
    Funzione di costruzione del grafo di LangGraph.
    """

    graph = StateGraph(GraphState, read_next_node=True)

    # aggiungi nodi
    graph.add_node("guard", guard)
    graph.add_node("semantic_search", semantic_search)
    graph.add_node("load_schema", load_schema)
    graph.add_node("generator", generator)
    graph.add_node("executor", executor)
    graph.add_node("result_handler", result_handler)

    # entry point
    graph.set_entry_point("guard")
    # graph.set_entry_point("load_schema")
    # graph.set_entry_point("semantic_search")

    # collegamenti
    # graph.add_edge("load_user_question", "load_schema")
    # Arco CONDIZIONALE

    graph.add_conditional_edges(
        "guard",  # Da quale nodo parte
        choose_if_continue,  # Funzione che decide il percorso
        {
            "continue": "semantic_search",  # Se ritorna "retry", torna al nodo generatore
            "stop": END,  # Se ritorna "stop", l'esecuzione può terminare
        },
    )

    graph.add_edge("semantic_search", "load_schema")
    graph.add_edge("load_schema", "generator")
    graph.add_edge("generator", "executor")

    # Arco CONDIZIONALE
    graph.add_conditional_edges(
        "executor",  # Da quale nodo parte
        choose_if_retry,  # Funzione che decide il percorso
        {
            "retry": "generator",  # Se ritorna "retry", torna al nodo generatore
            "end": "result_handler",  # Se ritorna "end", vai al nodo handler per elaborare il risultato e terminare
        },
    )

    return graph.compile()
