# tools/scoring.py
import re
from data.skill_graph import SKILL_KEYWORDS, get_prerequisites
from data.resource_kb import get_semantic_similarity
from tools.intent_extractor import extract_intent

NEGATION_WORDS = {"not", "never", "don't", "doesn't", "didn't", "no", "without", "avoid"}


def compute_keyword_score(answer: str, skill: str,
                          dynamic_keywords: list[str] | None = None) -> float:
    """
    Keyword score with negation detection — 0 to 1.

    If dynamic_keywords are provided (from intent extractor), they take
    priority over the static SKILL_KEYWORDS for this skill. This makes
    scoring question-specific rather than generically skill-based.
    """
    keywords = dynamic_keywords if dynamic_keywords else SKILL_KEYWORDS.get(skill, [])
    if not keywords:
        return 0.5

    # Cap keyword list to prevent score dilution when multiple intent
    # triggers combine (e.g. a Webpack question matching 4 patterns
    # could produce 20+ keywords, making 5 matches look like 25%)
    MAX_KEYWORDS = 10
    keywords = keywords[:MAX_KEYWORDS]

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
                score -= 0.5  # penalize negated mentions
            else:
                score += 1
    return round(max(0.0, min(1.0, score / len(keywords))), 3)


def order_gaps_by_prerequisites(gaps: list[str]) -> list[str]:
    def prereq_count(skill):
        prereqs = get_prerequisites(skill)
        return sum(1 for p in prereqs if p in gaps)
    return sorted(gaps, key=prereq_count)


def score_answer(answer: str, skill: str, question: str = "",
                 gemini_fn=None) -> dict:
    """Wrapper so evaluator.py can call a clean interface."""
    return compute_hybrid_score(0.0, skill, answer,
                                question=question, gemini_fn=gemini_fn)


def compute_hybrid_score(llm_score: float, skill: str, answer: str,
                         question: str = "", gemini_fn=None) -> dict:
    """
    Question-aware Hybrid Scoring Engine.

    Flow:
      1. If a question is provided, extract its intent deterministically.
      2. Use question-specific target + keywords for semantic/keyword scoring.
      3. LLM is only called when intent confidence is LOW (question was vague /
         no triggers matched) OR when semantic and keyword strongly disagree.
      4. Fall back to generic gold-standard + SKILL_KEYWORDS if no question given.

    Weights:
      Semantic similarity : 50%
      Keyword coverage    : 30%
      LLM score           : 20%  (only when needed — saves API quota)
    """
    intent_used = False
    confidence = 0.0
    dynamic_keywords: list[str] | None = None

    # ── Step 1: Extract question intent (deterministic, no LLM) ──────────────
    # Always compute gold-standard semantic as a baseline safety net
    gold_semantic = get_semantic_similarity(answer, skill)

    if question:
        intent = extract_intent(question, skill)
        confidence = intent["confidence"]

        if intent["target_text"]:
            # Question-specific semantic target
            intent_semantic = get_semantic_similarity(
                answer, skill, target_text=intent["target_text"]
            )
            # Take the BETTER of the two scores.
            # If our intent reference is wrong for this question type
            # (e.g. Enzyme debounce ref vs lifecycle question), the gold
            # standard catches it. If the intent ref is spot-on, it wins.
            semantic_score = max(intent_semantic, gold_semantic)

            # Merge dynamic keywords with static ones (deduped, capped)
            static_kw = SKILL_KEYWORDS.get(skill, [])
            merged = list(intent["keywords"])
            for kw in static_kw:
                if kw not in merged:
                    merged.append(kw)
            dynamic_keywords = merged  # capping happens in compute_keyword_score

            intent_used = True
        else:
            # Intent extractor found no triggers — fall back to gold standard
            semantic_score = gold_semantic
    else:
        semantic_score = gold_semantic

    # ── Step 2: Keyword scoring ───────────────────────────────────────────────
    keyword_score = compute_keyword_score(answer, skill,
                                          dynamic_keywords=dynamic_keywords)

    # ── Step 3: Decide whether to call LLM ───────────────────────────────────
    llm_normalized = llm_score / 5.0
    llm_called = False

    agreement = abs(semantic_score - keyword_score)
    zero_confidence = confidence == 0.0     # intent extractor understood nothing
    low_confidence  = confidence < 0.5      # partial understanding

    if gemini_fn:
        if zero_confidence:
            # Complete intent failure — deterministic scoring is unreliable.
            # The question may not even match the skill (e.g. A/B testing
            # question scored as "Jest"). LLM is the only signal that can
            # understand the question-answer pair in context.
            llm_normalized = gemini_fn(answer, skill)
            llm_called = True
            # Elevate LLM weight since semantic/keyword used wrong references
            weighted = (
                0.20 * semantic_score +
                0.10 * keyword_score +
                0.70 * llm_normalized
            )
        elif low_confidence and agreement >= 0.25:
            # Partial intent match + disagreeing signals — LLM tiebreaker
            llm_normalized = gemini_fn(answer, skill)
            llm_called = True

    # ── Step 4: Weighted combination ─────────────────────────────────────────
    if not (zero_confidence and llm_called):
        # Normal weighting (intent extractor worked or LLM wasn't called)
        weighted = (
            0.50 * semantic_score +
            0.30 * keyword_score +
            0.20 * llm_normalized
        )

    return {
        "llm":            round(llm_normalized, 3),
        "semantic":       round(semantic_score, 3),
        "keyword":        round(keyword_score, 3),
        "final_score":    round(weighted, 3),
        "llm_called":     llm_called,
        "intent_used":    intent_used,
        "confidence":     confidence,
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