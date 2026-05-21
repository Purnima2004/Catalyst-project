"""
Evaluator Agent
────────────────
Uses the Hybrid Scoring Engine:
  - Semantic score (50%) — ChromaDB distance vs gold-standard answer
  - Keyword score  (30%) — technical term coverage
  - LLM score    (20%) — qualitative depth assessment
"""

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field

from tools.scoring import score_answer, score_to_proficiency
from .state import CatalystState, SkillEvaluation

_llm = None



def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
    return _llm

_SYSTEM_PROMPT = """
You are a strict technical interview assessor. Score this answer from 0 to 5.

Skill being assessed: {skill}
Interview question: {question}
Candidate's answer: {answer}

Scoring rubric:
- 5: Expert level, production tradeoffs, edge cases, best practices
- 4: Strong, correct approach, minor gaps
- 3: Correct basics, missing depth or real-world application
- 2: Partial understanding, some correct concepts mixed with gaps
- 1: Aware of topic but minimal real knowledge
- 0: Wrong, off-topic, or no answer

Reply with ONLY valid JSON containing "score" and "reasoning", e.g. {{"score": 4.0, "reasoning": "Candidate gave a strong answer but missed tradeoffs."}}
"""


class _LLMEvaluation(BaseModel):
    score: float = Field(description="Score from 0.0 to 5.0")
    reasoning: str = Field(description="Brief explanation for the score")



def _llm_score(answer: str, skill: str, question: str = "") -> float:
    """
    LLM primary scorer — provides the main qualitative assessment.
    """
    structured_llm = _get_llm().with_structured_output(_LLMEvaluation, method="json_mode")
    
    # We now format the system prompt dynamically with the context
    eval_prompt = _SYSTEM_PROMPT.format(
        skill=skill,
        question=question if question else "Not provided.",
        answer=answer
    )
    
    result = structured_llm.invoke([
        SystemMessage(content="You are a strict technical evaluator. Output only JSON."),
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
    def _llm_score_with_ctx(answer: str, skill: str) -> float:
        return _llm_score(answer, skill, question=question_text)

    # Question-aware hybrid scoring
    scores = score_answer(answer_text, current_skill,
                          question=question_text,
                          llm_fn=_llm_score_with_ctx)

    # Convert 0-1 score back to 0-5 scale for display
    final_5 = round(scores["final_score"] * 5, 2)
    sem_5   = round(scores["semantic"] * 5, 2)
    kw_5    = round(scores["keyword"] * 5, 2)
    llm_5   = round((scores["llm"] * 5), 2) if scores["llm"] is not None else None

    proficiency = score_to_proficiency(final_5)
    
    if scores.get("gated"):
        mode_str = "gated (fast pass/fail)"
        llm_val = "Skipped"
    else:
        mode_str = "LLM-primary (20/20/60)"
        llm_val = f"{llm_5}/5"
        
    reasoning = (f"Semantic: {sem_5}/5 | Keyword: {kw_5}/5 | "
                 f"LLM: {llm_val} | Mode: {mode_str}")

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
