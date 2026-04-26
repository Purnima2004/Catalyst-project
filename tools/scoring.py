from data.skill_graph import SKILL_KEYWORDS
from data.resource_kb import get_semantic_similarity


def compute_keyword_score(answer: str, skill: str) -> float:
    """Score 0-1 based on fraction of expected keywords found in answer."""
    keywords = SKILL_KEYWORDS.get(skill, [])
    if not keywords:
        return 0.5  # neutral if no keywords defined
    answer_lower = answer.lower()
    hits = sum(1 for kw in keywords if kw.lower() in answer_lower)
    return round(hits / len(keywords), 3)


def compute_hybrid_score(llm_score: float, skill: str, answer: str) -> dict:
    """
    Combine 3 scoring signals into a final score (0-5).
      - LLM score    : 50% weight (already 0-5, normalize to 0-1)
      - Semantic sim : 30% weight (0-1 from ChromaDB distance)
      - Keyword cov  : 20% weight (0-1 from keyword matching)
    """
    semantic_score = get_semantic_similarity(answer, skill)
    keyword_score = compute_keyword_score(answer, skill)

    llm_normalized = llm_score / 5.0
    weighted = (
        0.50 * llm_normalized +
        0.30 * semantic_score +
        0.20 * keyword_score
    )
    final_score = round(weighted * 5.0, 2)  # back to 0-5 scale

    return {
        "llm_score": round(llm_score, 2),
        "semantic_score": round(semantic_score * 5.0, 2),
        "keyword_score": round(keyword_score * 5.0, 2),
        "final_score": final_score,
    }


def score_to_proficiency(score: float) -> str:
    if score >= 4.0:
        return "Expert"
    elif score >= 3.0:
        return "Advanced"
    elif score >= 2.0:
        return "Intermediate"
    else:
        return "Novice"
