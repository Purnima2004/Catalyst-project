import operator
from typing import Annotated, TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage


class SkillEvaluation(TypedDict):
    skill: str
    llm_score: float
    semantic_score: float
    keyword_score: float
    final_score: float
    proficiency: str
    reasoning: str


class CatalystState(TypedDict):
    # Inputs
    job_description: str
    resume_text: str
    resume_hash: str
    is_returning_user: bool

    # Skill Extractor output
    skills_to_assess: List[str]

    # Interview loop state
    current_skill_index: int
    messages: Annotated[List[BaseMessage], operator.add]

    # Evaluator output
    evaluations: List[SkillEvaluation]

    # Mentor output
    learning_plan: str

    # Flow control
    interview_complete: bool
