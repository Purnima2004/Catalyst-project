from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import InterviewState
from .nodes import (
    extract_skills_node,
    generate_question_node,
    evaluate_answer_node,
    generate_learning_plan_node
)

def human_node(state: InterviewState):
    """Dummy node to represent user input pause."""
    return {}

def route_after_evaluation(state: InterviewState):
    skills = state.get("skills_to_assess", [])
    idx = state.get("current_skill_index", 0)
    if idx >= len(skills):
        return "generate_learning_plan"
    return "generate_question"

def build_graph():
    workflow = StateGraph(InterviewState)
    
    # Add nodes
    workflow.add_node("extract_skills", extract_skills_node)
    workflow.add_node("generate_question", generate_question_node)
    workflow.add_node("human", human_node)
    workflow.add_node("evaluate_answer", evaluate_answer_node)
    workflow.add_node("generate_learning_plan", generate_learning_plan_node)
    
    # Add edges
    workflow.set_entry_point("extract_skills")
    workflow.add_edge("extract_skills", "generate_question")
    workflow.add_edge("generate_question", "human")
    workflow.add_edge("human", "evaluate_answer")
    
    # Conditional routing after evaluation
    workflow.add_conditional_edges(
        "evaluate_answer",
        route_after_evaluation,
        {
            "generate_learning_plan": "generate_learning_plan",
            "generate_question": "generate_question"
        }
    )
    workflow.add_edge("generate_learning_plan", END)
    
    # Compile with memory checkpointer
    memory = MemorySaver()
    # Interrupt execution before the 'human' node to wait for user input
    graph = workflow.compile(checkpointer=memory, interrupt_before=["human"])
    
    return graph

# Export a compiled instance
graph = build_graph()
