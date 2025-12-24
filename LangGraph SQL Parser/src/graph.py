from langgraph.graph import StateGraph, END
from state import GraphState
from nodes.load_user_question import load_user_question
from nodes.load_schema import load_schema
from nodes.generator import generator
from nodes.executor import executor
from nodes.router import router
from nodes.router2 import router2
from nodes.result_handler import result_handler


def build_graph():
    graph = StateGraph(GraphState, read_next_node=True)

    # aggiungi nodi
    graph.add_node("load_user_question", load_user_question)
    graph.add_node("load_schema", load_schema)
    graph.add_node("generator", generator)
    graph.add_node("executor", executor)
    graph.add_node("result_handler", result_handler)

    # entry point
    graph.set_entry_point("load_user_question")
    #graph.set_entry_point("load_schema")

    # collegamenti sequenziali
   # graph.add_edge("load_user_question", "load_schema")
     # Arco CONDIZIONALE
    graph.add_conditional_edges(
        "load_user_question",  # Da quale nodo parte
        router2,  # Funzione che decide il percorso
        {
            "continue": "load_schema",  # Se ritorna "retry", torna al nodo generatore
            "end": "result_handler",  # Se ritorna "end", vai al nodo handler per elaborare il risultato e terminare
        },
    )
    graph.add_edge("load_schema", "generator")
    graph.add_edge("generator", "executor")

    # Arco CONDIZIONALE
    graph.add_conditional_edges(
        "executor",  # Da quale nodo parte
        router,  # Funzione che decide il percorso
        {
            "retry": "generator",  # Se ritorna "retry", torna al nodo generatore
            "end": "result_handler",  # Se ritorna "end", vai al nodo handler per elaborare il risultato e terminare
        },
    )

    return graph.compile()
