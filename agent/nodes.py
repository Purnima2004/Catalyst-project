import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field
from .state import InterviewState, SkillEvaluation

# Use gemini-1.5-pro or equivalent capable model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)

class ExtractedSkills(BaseModel):
    skills: list[str] = Field(description="List of 3 to 5 core skills to assess based on JD and Resume gaps")

class AnswerEvaluation(BaseModel):
    score: int = Field(description="Score from 0 to 5")
    proficiency: str = Field(description="Proficiency level: Novice, Intermediate, Advanced, Expert")
    reasoning: str = Field(description="Explanation for the score and proficiency")
    follow_up_needed: bool = Field(description="True if more questions are needed for this skill, False otherwise")

def extract_skills_node(state: InterviewState):
    """Extracts skills to assess from JD and Resume."""
    jd = state.get("job_description", "")
    resume = state.get("resume_text", "")
    
    prompt = f"""
    You are an expert technical recruiter. Review the Job Description and the candidate's Resume.
    Identify 3 to 5 core technical skills that are required by the JD.
    Prioritize skills where the candidate's resume shows potential gaps or requires verification of actual proficiency.
    
    Job Description:
    {jd}
    
    Resume:
    {resume}
    """
    
    structured_llm = llm.with_structured_output(ExtractedSkills)
    result = structured_llm.invoke([SystemMessage(content=prompt)])
    
    return {"skills_to_assess": result.skills, "current_skill_index": 0}

def generate_question_node(state: InterviewState):
    """Generates the next interview question based on the current skill."""
    skills = state.get("skills_to_assess", [])
    idx = state.get("current_skill_index", 0)
    
    if idx >= len(skills):
        return {"interview_complete": True}
        
    current_skill = skills[idx]
    messages = state.get("messages", [])
    
    prompt = f"""
    You are an expert technical interviewer assessing a candidate's real-world proficiency in: {current_skill}.
    Generate an open-ended, scenario-based interview question to test their actual experience, not just trivia.
    Keep the question conversational and concise (1-2 sentences).
    Do not greet the candidate or provide context, just ask the question directly.
    """
    
    # We only pass the last few messages so the LLM doesn't get confused by previous skill questions
    recent_messages = messages[-4:] if len(messages) >= 4 else messages
    response = llm.invoke([SystemMessage(content=prompt)] + recent_messages)
    
    return {"messages": [response]}

def evaluate_answer_node(state: InterviewState):
    """Evaluates the candidate's answer and moves to the next skill."""
    skills = state.get("skills_to_assess", [])
    idx = state.get("current_skill_index", 0)
    current_skill = skills[idx]
    
    messages = state.get("messages", [])
    
    prompt = f"""
    You are an expert technical assessor. Evaluate the candidate's response to the interview question about the skill: {current_skill}.
    
    Analyze their answer for depth, practical experience, and correctness.
    Score them from 0 to 5 and assign a proficiency level (Novice, Intermediate, Advanced, Expert).
    Determine if you have enough signal to stop assessing this skill (follow_up_needed = False), or if you need to ask a follow-up question to be sure (follow_up_needed = True).
    """
    
    structured_llm = llm.with_structured_output(AnswerEvaluation)
    # Give the evaluator the last question and answer pair
    context_msgs = messages[-2:] if len(messages) >= 2 else messages
    result = structured_llm.invoke([SystemMessage(content=prompt)] + context_msgs)
    
    evaluation = SkillEvaluation(
        skill=current_skill,
        score=result.score,
        proficiency=result.proficiency,
        reasoning=result.reasoning
    )
    
    evaluations = state.get("evaluations", [])
    evaluations.append(evaluation)
    
    return {
        "evaluations": evaluations,
        "current_skill_index": idx + 1
    }

def generate_learning_plan_node(state: InterviewState):
    """Generates the final learning plan based on gaps."""
    evaluations = state.get("evaluations", [])
    jd = state.get("job_description", "")
    
    eval_text = "\n".join([f"Skill: {e['skill']}, Proficiency: {e['proficiency']} (Score {e['score']}/5)\nReasoning: {e['reasoning']}" for e in evaluations])
    
    prompt = f"""
    You are a career mentor. Based on the Job Description and the candidate's interview evaluations, identify their skill gaps.
    Generate a highly personalized, actionable learning plan focused on acquiring the missing or adjacent skills they need to succeed in this role.
    
    For each gap, provide:
    1. A specific goal.
    2. Curated resource types (e.g., "Build a mini-project doing X", "Read this specific documentation").
    3. Realistic time estimates (e.g., 10 hours).
    
    Format the output in clean, readable Markdown.
    
    Job Description:
    {jd}
    
    Evaluations:
    {eval_text}
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    
    return {"learning_plan": response.content}
