import streamlit as st
import uuid
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

# Load .env for local dev
load_dotenv()

# On Streamlit Cloud, read the API key from st.secrets and inject into env
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"].strip()
elif os.environ.get("GOOGLE_API_KEY"):
    # Strip any accidental leading/trailing whitespace from .env file
    os.environ["GOOGLE_API_KEY"] = os.environ["GOOGLE_API_KEY"].strip()

from utils.pdf_parser import extract_text_from_pdf
from data.candidate_store import hash_bytes, get_candidate, save_candidate
from agents.supervisor import graph

# --- Page Config ---
st.set_page_config(
    page_title="Catalyst | AI Skill Assessor",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0e1117; color: #f4f4f5; }
.stSidebar { background: #0e1117 !important; border-right: 1px solid #27272a; }

.hero-title {
    font-size: 2.2rem; font-weight: 600; letter-spacing: -0.02em;
    color: #ffffff; margin-bottom: 0.2rem;
}
.hero-sub { font-size: 0.95rem; color: #a1a1aa; font-weight: 300; margin-bottom: 2rem; }

.stButton>button {
    background: #18181b; color: #e4e4e7; 
    border: 1px solid #3f3f46; border-radius: 6px;
    font-weight: 500; font-size: 0.9rem; padding: 0.5rem 1rem;
    transition: all 0.2s ease;
}
.stButton>button:hover {
    background: #27272a; border-color: #52525b; color: #ffffff;
}

[data-testid="stChatMessage"] {
    background: transparent;
    border: none;
    border-bottom: 1px solid #27272a;
    border-radius: 0; padding: 1.5rem 0; margin-bottom: 0;
}

.score-card {
    background: transparent;
    border: 1px solid #27272a;
    border-radius: 6px; padding: 1.2rem; margin: 0.5rem 0;
}
.score-card h4 {
    font-size: 1rem; font-weight: 500; color: #ffffff; margin-top: 0; margin-bottom: 0.5rem;
}
.score-bar-container { background: #27272a; border-radius: 2px; height: 4px; margin: 8px 0; }
.score-bar { height: 4px; border-radius: 2px; }

.pill-returning, .pill-new {
    display: inline-block; padding: 0.15rem 0.5rem;
    background: transparent; border-radius: 4px;
    font-size: 0.75rem; font-weight: 500; margin-bottom: 0.5rem;
}
.pill-returning { border: 1px solid rgba(52, 211, 153, 0.4); color: #34d399; }
.pill-new { border: 1px solid rgba(129, 140, 248, 0.4); color: #818cf8; }
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.started = False
    st.session_state.returning = False

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# --- Header ---
st.markdown('<p class="hero-title">Catalyst</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">AI-Powered Skill Assessment & Personalised Learning Plan Agent</p>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### Start Assessment")
    st.divider()
    job_description = st.text_area(
        "Job Description",
        height=220,
        placeholder="Paste the full JD here...",
        key="jd_input"
    )
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if resume_file:
        pdf_bytes = resume_file.read()
        resume_hash = hash_bytes(pdf_bytes)
        cached = get_candidate(resume_hash)

        if cached:
            st.markdown('<span class="pill-returning">Returning User — Resume Loaded from Cache</span>', unsafe_allow_html=True)
            st.session_state.returning = True
            resume_text = cached["resume_text"]
        else:
            st.markdown('<span class="pill-new">New Resume Detected</span>', unsafe_allow_html=True)
            st.session_state.returning = False
            resume_text = extract_text_from_pdf(pdf_bytes)
            save_candidate(resume_hash, resume_text)

        st.session_state.resume_text = resume_text
        st.session_state.resume_hash = resume_hash

    st.divider()
    start_btn = st.button("Start Assessment", use_container_width=True, type="primary")

# --- Start Assessment ---
if start_btn and job_description and st.session_state.get("resume_text"):
    with st.spinner("Analysing profile and identifying core skills..."):
        initial_state = {
            "job_description": job_description,
            "resume_text": st.session_state.resume_text,
            "resume_hash": st.session_state.resume_hash,
            "is_returning_user": st.session_state.returning,
            "messages": [],
            "evaluations": [],
        }
        graph.invoke(initial_state, config)
        st.session_state.started = True

# --- Interview / Results ---
if st.session_state.get("started"):
    state = graph.get_state(config)

    if not state.next:
        # Assessment Complete
        st.success("Assessment Complete. Here is your personalised learning plan.")

        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("## Personalised Learning Plan")
            plan = state.values.get("learning_plan", "")
            st.markdown(plan)

        with col2:
            st.markdown("## Score Breakdown")
            evals = state.values.get("evaluations", [])
            for e in evals:
                pct = int((e["final_score"] / 5.0) * 100)
                color = "#34d399" if e["final_score"] >= 3.5 else "#fbbf24" if e["final_score"] >= 2.0 else "#f87171"
                st.markdown(f"""
<div class="score-card">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
    <span style="font-weight:500;color:#f4f4f5">{e['skill']}</span>
    <span style="color:{color};font-size:0.85rem;font-weight:500">{e['proficiency']} ({e['final_score']:.1f}/5)</span>
  </div>
  <div class="score-bar-container">
    <div class="score-bar" style="width:{pct}%;background:{color}"></div>
  </div>
  <div style="color:#a1a1aa;font-size:0.85rem;margin-top:6px;line-height:1.4;">{e['reasoning']}</div>
</div>
""", unsafe_allow_html=True)

    else:
        # Interview in progress
        messages = state.values.get("messages", [])
        skills = state.values.get("skills_to_assess", [])
        idx = state.values.get("current_skill_index", 0)

        progress = idx / len(skills) if skills else 0
        st.markdown(f"**Progress:** Skill {idx} of {len(skills)}")
        st.progress(progress)

        if skills and idx < len(skills):
            st.info(f"Currently assessing: **{skills[idx]}**")

        for msg in messages:
            if isinstance(msg, AIMessage):
                with st.chat_message("assistant"):
                    st.write(msg.content)
            elif isinstance(msg, HumanMessage):
                with st.chat_message("user"):
                    st.write(msg.content)

        user_input = st.chat_input("Type your answer here...")
        if user_input:
            with st.chat_message("user"):
                st.write(user_input)
            with st.spinner("Evaluating..."):
                graph.update_state(
                    config,
                    {"messages": [HumanMessage(content=user_input)]},
                    as_node="human"
                )
                graph.invoke(None, config)
            st.rerun()

elif not st.session_state.get("started"):
    # Landing state
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
<div class="score-card">
  <h4>Skill Knowledge Graph</h4>
  <p style="color:#a1a1aa;font-size:0.85rem;line-height:1.5;">
    50+ skills mapped with relationships. Deterministic gap analysis
    — no LLM hallucinations for skill identification.
  </p>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="score-card">
  <h4>Hybrid Scoring Engine</h4>
  <p style="color:#a1a1aa;font-size:0.85rem;line-height:1.5;">
    3-signal evaluation: LLM qualitative score + semantic similarity
    + keyword coverage. Objective and explainable.
  </p>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class="score-card">
  <h4>RAG Resource Curator</h4>
  <p style="color:#a1a1aa;font-size:0.85rem;line-height:1.5;">
    Learning plan grounded in 35+ real, curated resources.
    No hallucinated links — ever.
  </p>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Paste a Job Description and upload your Resume in the sidebar to begin your assessment.")
