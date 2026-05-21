# tools/scoring.py
import re
from data.skill_graph import SKILL_KEYWORDS, get_prerequisites
from data.resource_kb import get_semantic_similarity


NEGATION_WORDS = {"not", "never", "don't", "doesn't", "didn't", "no", "without", "avoid"}


def _keyword_hit(kw_lower: str, answer_lower: str) -> bool:
    """
    Flexible keyword match that handles three cases:
      1. Single-word keywords  → strict word boundary (\b)
      2. Multi-word phrases    → phrase present anywhere in text (no boundary needed
                                 since spaces already delimit naturally)
      3. Prefix matches        → e.g. "pg_stat" matches "pg_stat_statements"
                                 because underscore is a word char and \b fails.
                                 We do a simple substring check for tokens
                                 that contain underscores.
    Negation check is applied only for single-word keywords (phrase negation is
    too rare to be worth the complexity).
    """
    if kw_lower not in answer_lower:
        return False, False   # (hit, negated)

    # Underscore-containing tokens (e.g. pg_stat, pg_locks): substring is enough
    if "_" in kw_lower:
        return True, False

    # Multi-word phrase: presence in text is sufficient
    if " " in kw_lower:
        # Check negation: look at the 3 words before the phrase
        idx = answer_lower.find(kw_lower)
        preceding = answer_lower[:idx].split()[-3:]
        negated = any(neg in preceding for neg in NEGATION_WORDS)
        return True, negated

    # Single word: require word boundary
    match = re.search(rf'\b{re.escape(kw_lower)}\b', answer_lower)
    if not match:
        return False, False
    preceding = answer_lower[:match.start()].split()[-3:]
    negated = any(neg in preceding for neg in NEGATION_WORDS)
    return True, negated


def compute_keyword_score(answer: str, skill: str,
                          dynamic_keywords: list[str] | None = None) -> float:
    """
    Keyword score with negation detection and flexible matching — 0 to 1.
    """
    keywords = dynamic_keywords
    if not keywords:
        keywords = SKILL_KEYWORDS.get(skill)
        
    # Fallback for combined names like "Advanced SQL & Database Design"
    if not keywords:
        for known_skill, kw_list in SKILL_KEYWORDS.items():
            if known_skill.lower() in skill.lower():
                keywords = kw_list
                break

    if not keywords:
        return 0.5

    MAX_KEYWORDS = 15
    keywords = keywords[:MAX_KEYWORDS]

    answer_lower = answer.lower()
    score = 0.0
    for kw in keywords:
        kw_lower = kw.lower()
        hit, negated = _keyword_hit(kw_lower, answer_lower)
        if hit:
            score += -0.5 if negated else 1.0

    # You don't need to hit every single keyword to be an expert.
    # Hitting ~40% of the relevant keywords in a short answer is excellent.
    expected_hits = min(len(keywords), 5)
    
    return round(max(0.0, min(1.0, score / expected_hits)), 3)


def order_gaps_by_prerequisites(gaps: list[str]) -> list[str]:
    def prereq_count(skill):
        prereqs = get_prerequisites(skill)
        return sum(1 for p in prereqs if p in gaps)
    return sorted(gaps, key=prereq_count)


def quick_gate(answer: str, skill: str) -> float | None:
    """
    Fast pass/fail for obvious cases.
    Returns a 0-1 score, or None to proceed to full pipeline.
    """
    answer_stripped = answer.strip()
    if len(answer_stripped) < 50:
        return 0.15   # ~0.75/5 — too short

    keywords = SKILL_KEYWORDS.get(skill, [])
    if not keywords:
        return None   # unknown skill — let LLM handle it

    answer_lower = answer.lower()
    hits = sum(1 for kw in keywords if kw.lower() in answer_lower)
    hit_ratio = hits / len(keywords)

    if hit_ratio >= 0.70:
        return 0.82   # ~4.1/5 — clearly an expert

    if hits == 0 and len(answer_stripped) < 200:
        return 0.15   # ~0.75/5 — short answer with zero keywords

    return None


def score_answer(answer: str, skill: str, question: str = "",
                 llm_fn=None) -> dict:
    """Wrapper so evaluator.py can call a clean interface."""
    return compute_hybrid_score(0.0, skill, answer,
                                question=question, llm_fn=llm_fn)


def compute_hybrid_score(llm_score: float, skill: str, answer: str,
                         question: str = "", llm_fn=None) -> dict:
    """
    3-layer scoring:
      1. Quick Gate  — instant score for obvious pass/fail (no LLM call)
      2. Full Pipeline:
           Semantic  20%  — ChromaDB multi-reference cosine similarity
           Keyword   20%  — flexible term coverage
           LLM       60%  — primary qualitative assessor
    """
    gated_score = quick_gate(answer, skill)
    if gated_score is not None:
        return {
            "llm": None,
            "semantic": gated_score,
            "keyword": gated_score,
            "final_score": gated_score,
            "llm_called": False,
            "intent_used": False,
            "confidence": 1.0,
            "gated": True
        }

    semantic_score = get_semantic_similarity(answer, skill)
    keyword_score  = compute_keyword_score(answer, skill)

    llm_normalized = llm_score / 5.0
    llm_called = False

    if llm_fn:
        llm_normalized = llm_fn(answer, skill)
        llm_called = True

    weighted = (
        0.20 * semantic_score +
        0.20 * keyword_score +
        0.60 * llm_normalized
    )

    return {
        "llm":         round(llm_normalized, 3) if llm_called else None,
        "semantic":    round(semantic_score, 3),
        "keyword":     round(keyword_score, 3),
        "final_score": round(weighted, 3),
        "llm_called":  llm_called,
        "intent_used": False,
        "confidence":  1.0,
        "gated":       False
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