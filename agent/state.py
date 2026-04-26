import operator
from typing import Annotated, TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage

class SkillEvaluation(TypedDict):
    skill: str
    score: int  # 0 to 5
    proficiency: str # Novice, Intermediate, Advanced, Expert
    reasoning: str

class InterviewState(TypedDict):
    job_description: str
    resume_text: str
    skills_to_assess: List[str]
    current_skill_index: int
    messages: Annotated[List[BaseMessage], operator.add]
    evaluations: List[SkillEvaluation]
    learning_plan: str
    interview_complete: bool
