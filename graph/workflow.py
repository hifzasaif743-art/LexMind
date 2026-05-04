from langgraph.graph import StateGraph, END
from graph.state import LegalAIState
from agents.router_agent import RouterAgent
from agents.rag_agent import RAGAgent
from agents.general_agent import GeneralAgent
from agents.task_agent import TaskAgent
from agents.evaluator_agent import EvaluatorAgent

router_agent = RouterAgent()
rag_agent = RAGAgent()
general_agent = GeneralAgent()
task_agent = TaskAgent()
evaluator_agent = EvaluatorAgent()

def router_node(state): return router_agent.run(state)
def rag_node(state): return rag_agent.run(state)
def general_node(state): return general_agent.run(state)
def task_node(state): return task_agent.run(state)
def evaluator_node(state): return evaluator_agent.run(state)

def final_node(state):
    footer = {"rag": "\n\n---\n_Based on your document._", "general": "\n\n---\n_General info only._", "task": "\n\n---\n_Structured analysis._"}.get(state["query_type"], "")
    return {"final_response": state["agent_response"] + footer}

def route_after_router(state): return state["query_type"]

def route_after_evaluator(state):
    if state["evaluation_result"] == "pass" or state.get("retry_count", 0) >= 3:
        return "final"
    return state["query_type"]

def build_graph():
    graph = StateGraph(LegalAIState)
    graph.add_node("router", router_node)
    graph.add_node("rag", rag_node)
    graph.add_node("general", general_node)
    graph.add_node("task", task_node)
    graph.add_node("evaluator", evaluator_node)
    graph.add_node("final", final_node)
    graph.set_entry_point("router")
    graph.add_conditional_edges("router", route_after_router, {"rag": "rag", "general": "general", "task": "task"})
    graph.add_edge("rag", "evaluator")
    graph.add_edge("general", "evaluator")
    graph.add_edge("task", "evaluator")
    graph.add_conditional_edges("evaluator", route_after_evaluator, {"rag": "rag", "general": "general", "task": "task", "final": "final"})
    graph.add_edge("final", END)
    return graph.compile()