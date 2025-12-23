from langgraph.graph import StateGraph, END
from state import GraphState
from nodes.load_user_question import load_user_question
from nodes.load_schema import load_schema
from nodes.generator import generator
from nodes.executor import executor
from nodes.router import router
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

    # collegamenti sequenziali
    graph.add_edge("load_user_question", "load_schema")
    graph.add_edge("load_schema", "generator")
    graph.add_edge("generator", "executor")
    # graph.add_edge("executor","result_handler")

    # Arco CONDIZIONALE
    graph.add_conditional_edges(
        "executor",  # Da quale nodo parte
        router,  # Funzione che decide il percorso
        {
            "retry": "generator",  # Se ritorna "continue", torna a nodo_1
            "end": "result_handler",  # Se ritorna "end", termina
        },
    )

    return graph.compile()
