"""
Supervisor — Main LangGraph orchestrator
──────────────────────────────────────────
Routes between 4 dedicated agents:
  skill_extractor → interviewer ⇄ [human] → evaluator → mentor → END
"""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from agents import skill_extractor, interviewer, evaluator, mentor
from agents.state import CatalystState


def _human_node(state: CatalystState) -> dict:
    """Placeholder node — execution pauses here to collect user input."""
    return {}


def _route_after_evaluation(state: CatalystState) -> str:
    skills = state.get("skills_to_assess", [])
    idx = state.get("current_skill_index", 0)
    if idx >= len(skills):
        return "mentor"
    return "interviewer"


def build_graph():
    workflow = StateGraph(CatalystState)

    # Register nodes — each agent is its own module with its own LLM
    workflow.add_node("skill_extractor", skill_extractor.run)
    workflow.add_node("interviewer", interviewer.run)
    workflow.add_node("human", _human_node)
    workflow.add_node("evaluator", evaluator.run)
    workflow.add_node("mentor", mentor.run)

    # Wire edges
    workflow.set_entry_point("skill_extractor")
    workflow.add_edge("skill_extractor", "interviewer")
    workflow.add_edge("interviewer", "human")
    workflow.add_edge("human", "evaluator")
    workflow.add_conditional_edges(
        "evaluator",
        _route_after_evaluation,
        {"mentor": "mentor", "interviewer": "interviewer"},
    )
    workflow.add_edge("mentor", END)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory, interrupt_before=["human"])


graph = build_graph()
