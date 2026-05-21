"""
Mentor Agent
─────────────
Generates a personalised learning plan using:
  - RAG: retrieves REAL curated resources from ChromaDB
  - Skill Knowledge Graph: suggests adjacent skills to learn
  - LLM: formats everything into clean, actionable markdown
"""
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from data.resource_kb import get_resources_for_skill
from data.skill_graph import get_adjacent_skills, get_prerequisites
from .state import CatalystState
from tools.scoring import order_gaps_by_prerequisites

import logging
logger = logging.getLogger(__name__)

# Lazy-loaded LLM — created on first call, not at import time
_llm = None

def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    return _llm

_SYSTEM_PROMPT = """
You are a world-class career mentor and learning coach.
You create highly personalised, actionable learning plans.
You are honest about skill gaps and encouraging about growth.
Format your output in clean Markdown with headers, bullet points, and time estimates.
"""

def run(state: CatalystState) -> dict:
    evaluations = state.get("evaluations", [])
    jd = state.get("job_description", "")

    # Temporarily add this at the start of mentor run()
    for e in evaluations:
        logger.warning(f"DEBUG SCORE >> {e['skill']}: final_score={e['final_score']}, proficiency={e['proficiency']}")

    # Build evaluation summary
    eval_lines = []
    for e in evaluations:
        eval_lines.append(
            f"- **{e['skill']}**: {e['proficiency']} "
            f"(Final Score: {e['final_score']}/5 | "
            f"LLM: {e['llm_score']}/5, Semantic: {e['semantic_score']}/5, Keywords: {e['keyword_score']}/5)\n"
            f"  Assessment: {e['reasoning']}"
        )

    # Build RAG-retrieved resources section
    resource_lines = []
    adjacent_lines = []
    has_weak_skills = False
    
    for e in evaluations:
        if e["final_score"] < 3.5:  # Only plan for weak skills
            has_weak_skills = True
            skill = e["skill"]
            resources = get_resources_for_skill(skill, score=e["final_score"], top_k=3)
            if resources:
                resource_lines.append(f"\n### Resources for {skill}")
                for r in resources:
                    resource_lines.append(
                        f"- [{r['title']}]({r['url']}) · *{r['type']}* · ~{r['hours']}h"
                    )

            # Adjacent skills from graph
            adj = get_adjacent_skills(skill)
            prereqs = get_prerequisites(skill)
            if adj or prereqs:
                adjacent_lines.append(f"- **{skill}** → adjacent: {', '.join(adj[:3])}")

    if resource_lines:
        resources_text = "\n".join(resource_lines)
    elif has_weak_skills:
        resources_text = "No curated resources found in the knowledge base for these specific skills. Please suggest high-quality official documentation and tutorials."
    else:
        resources_text = "No specific resources needed — strong across all assessed skills!"
    adjacent_text = "\n".join(adjacent_lines) if adjacent_lines else ""

    prompt = f"""
You are reviewing a candidate's technical assessment results. Based on the evaluation
below, generate a **personalised 4-6 week learning plan** to bridge their skill gaps
and prepare them for the target role.

**Job Description Context:**
{jd[:800]}

**Assessment Results:**
{chr(10).join(eval_lines)}

**Curated Learning Resources (from knowledge base):**
{resources_text}

**Adjacent Skills from Knowledge Graph to Consider:**
{adjacent_text}

Generate the full learning plan now. For each skill gap:
1. Set a clear weekly goal.
2. Reference the curated resources above (with links).
3. Suggest a hands-on project to apply the learning.
4. Give a realistic total time estimate.

End the plan with a "Strengths to Leverage" section.
"""

    response = _get_llm().invoke([
        SystemMessage(content=_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])

    return {"learning_plan": response.content}
