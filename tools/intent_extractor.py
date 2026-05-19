"""
Intent Extractor (Retired)
──────────────────────────
This module used to contain 500+ lines of regex patterns for question intent parsing.
It has been retired in favor of the 3-layer architecture:
1. Keyword gate (fast pass/fail)
2. ChromaDB multi-reference semantic scoring
3. LLM primary scoring

Do not use this file for new development. SKILL_KEYWORDS remains in data.skill_graph.
"""

def extract_intent(question: str, skill: str) -> dict:
    """Stub to prevent import errors if any old code still references this."""
    return {
        "target_text": "",
        "keywords": [],
        "confidence": 0.0
    }
