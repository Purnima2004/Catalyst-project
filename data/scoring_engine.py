# scoring_engine.py
import re
from resource_kb import get_semantic_similarity
from skill_graph import SKILL_KEYWORDS
from skill_graph import get_prerequisites

NEGATION_WORDS = {"not", "never", "don't", "doesn't", "didn't", "no", "without", "avoid", "never", "na"}

def keyword_score(answer: str, skill: str) -> float:
    keywords = SKILL_KEYWORDS.get(skill, [])
    if not keywords:
        return 0.5
    answer_lower = answer.lower()
    score = 0
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower not in answer_lower:
            continue
        match = re.search(rf'\b{re.escape(kw_lower)}\b', answer_lower)
        if match:
            preceding = answer_lower[:match.start()].split()[-3:]
            if any(neg in preceding for neg in NEGATION_WORDS):
                score -= 0.5
            else:
                score += 1
    return round(max(0.0, min(1.0, score / len(keywords))), 3)



def score_answer(answer: str, skill: str, gemini_fn=None) -> dict:
    """
    gemini_fn: optional callable(answer, skill) -> float (0-1)
    Only called when semantic and keyword scores disagree significantly.
    """
    sem = get_semantic_similarity(answer, skill)
    kw  = keyword_score(answer, skill)

    agreement = abs(sem - kw)
    llm_score = None
    llm_called = False

    if agreement >= 0.25 and gemini_fn:
        llm_score = gemini_fn(answer, skill)
        llm_called = True
        final = round((sem * 0.5) + (kw * 0.3) + (llm_score * 0.2), 3)
    else:
        final = round((sem * 0.5) + (kw * 0.3) + (0.5 * 0.2), 3)  # neutral LLM weight

    level = "beginner" if final < 0.4 else "intermediate" if final < 0.7 else "advanced"

    return {
        "skill": skill,
        "final_score": final,
        "semantic": sem,
        "keyword": kw,
        "llm": llm_score,
        "llm_called": llm_called,
        "level": level
    }

    
def order_gaps_by_prerequisites(gaps: list[str]) -> list[str]:
    """Sort gaps so prerequisites come before dependent skills."""
    def prereq_count(skill):
        prereqs = get_prerequisites(skill)
        return sum(1 for p in prereqs if p in gaps)
    
    return sorted(gaps, key=prereq_count)