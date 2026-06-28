from langgraph.graph import StateGraph, END

from agents.state import ResearchState
from agents.planner import planner_node
from agents.searcher import searcher_node
from agents.synthesizer import synthesizer_node


def build_graph() -> StateGraph:
    g = StateGraph(ResearchState)

    g.add_node("planner", planner_node)
    g.add_node("searcher", searcher_node)
    g.add_node("synthesizer", synthesizer_node)

    g.set_entry_point("planner")
    g.add_edge("planner", "searcher")
    g.add_edge("searcher", "synthesizer")
    g.add_edge("synthesizer", END)

    return g.compile()


research_graph = build_graph()
