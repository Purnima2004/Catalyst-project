"""
Evaluator Agent
────────────────
Uses the Hybrid Scoring Engine:
  - Semantic score (50%) — ChromaDB distance vs gold-standard answer
  - Keyword score  (30%) — technical term coverage
  - LLM score    (20%) — qualitative depth assessment
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field

from tools.scoring import score_answer, score_to_proficiency
from .state import CatalystState, SkillEvaluation

_llm = None



def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    return _llm

_SYSTEM_PROMPT = """
You are an expert technical assessor. You evaluate interview answers strictly, honestly,
and objectively. No sugarcoating. You score from 0 to 5:
  0 = No knowledge / completely wrong
  1 = Aware of concept but no real experience
  2 = Basic usage, limited depth
  3 = Solid understanding, some gaps
  4 = Strong practical experience
  5 = Expert-level, deep nuanced knowledge
Provide a score and concise reasoning (2 sentences max).
"""


class _LLMEvaluation(BaseModel):
    score: float = Field(description="Score from 0.0 to 5.0")
    reasoning: str = Field(description="Brief explanation for the score")



def _gemini_score(answer: str, skill: str, question: str = "") -> float:
    """
    LLM fallback scorer — called only when intent confidence is low
    or semantic/keyword signals strongly disagree.
    Includes the original interview question for context-aware scoring.
    """
    structured_llm = _get_llm().with_structured_output(_LLMEvaluation)
    question_ctx = f"Interview question asked:\n{question}\n\n" if question else ""
    eval_prompt = f"Skill being assessed: {skill}\n\n{question_ctx}Candidate answer:\n{answer}"
    result = structured_llm.invoke([
        SystemMessage(content=_SYSTEM_PROMPT),
        HumanMessage(content=eval_prompt)
    ])
    return result.score / 5.0  # normalize to 0-1 for scoring_engine


def run(state: CatalystState) -> dict:
    skills = state.get("skills_to_assess", [])
    idx = state.get("current_skill_index", 0)

    if idx >= len(skills):
        return {}

    current_skill = skills[idx]
    messages = state.get("messages", [])

    # Extract the last Q&A pair (AI question + Human answer)
    context = messages[-2:] if len(messages) >= 2 else messages
    if not context:
        return {}

    # Extract both the interview question and the candidate's answer
    question_text = ""
    answer_text = ""
    for m in context:
        if isinstance(m, AIMessage):
            question_text = m.content
        elif isinstance(m, HumanMessage):
            answer_text = m.content

    if not answer_text:
        return {}

    # Build a question-aware LLM scorer closure that includes the question context
    def _gemini_score_with_ctx(answer: str, skill: str) -> float:
        return _gemini_score(answer, skill, question=question_text)

    # Question-aware hybrid scoring
    # Intent extractor uses the question to derive specific targets
    scores = score_answer(answer_text, current_skill,
                          question=question_text,
                          gemini_fn=_gemini_score_with_ctx)

    # Convert 0-1 score back to 0-5 scale for display
    final_5 = round(scores["final_score"] * 5, 2)
    sem_5   = round(scores["semantic"] * 5, 2)
    kw_5    = round(scores["keyword"] * 5, 2)
    llm_5   = round((scores["llm"] * 5), 2) if scores["llm"] else None

    proficiency = score_to_proficiency(final_5)
    intent_flag = "✓ question-aware" if scores.get("intent_used") else "gold-standard"
    reasoning = (f"Semantic: {sem_5}/5 | Keyword: {kw_5}/5 | "
                 f"LLM called: {scores['llm_called']} | Mode: {intent_flag}")

    evaluation = SkillEvaluation(
        skill=current_skill,
        llm_score=llm_5 or 0.0,
        semantic_score=sem_5,
        keyword_score=kw_5,
        final_score=final_5,
        proficiency=proficiency,
        reasoning=reasoning,
    )

    existing = list(state.get("evaluations", []))
    existing.append(evaluation)

    return {
        "evaluations": existing,
        "current_skill_index": idx + 1,
    }
