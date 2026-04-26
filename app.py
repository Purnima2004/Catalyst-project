import streamlit as st
import uuid
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0a0f1e; color: #e2e8f0; }
.stSidebar { background: #0f172a !important; border-right: 1px solid #1e293b; }

.hero-title {
    font-size: 2.8rem; font-weight: 700; letter-spacing: -1px;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.hero-sub { font-size: 1rem; color: #64748b; margin-bottom: 2rem; }

.stButton>button {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    color: white; border: none; border-radius: 10px;
    font-weight: 600; font-size: 0.95rem; padding: 0.6rem 1.2rem;
    transition: all 0.25s ease; box-shadow: 0 4px 15px rgba(99,102,241,0.3);
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99,102,241,0.5);
    color: white;
}

[data-testid="stChatMessage"] {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 14px; margin-bottom: 12px;
    backdrop-filter: blur(8px);
}

.score-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px; padding: 1rem; margin: 0.5rem 0;
}
.score-bar-container { background: #1e293b; border-radius: 99px; height: 8px; margin: 4px 0; }
.score-bar { height: 8px; border-radius: 99px; }

.pill-returning {
    display: inline-block; padding: 0.2rem 0.8rem;
    background: rgba(16,185,129,0.15); color: #10b981;
    border: 1px solid rgba(16,185,129,0.3); border-radius: 99px;
    font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem;
}
.pill-new {
    display: inline-block; padding: 0.2rem 0.8rem;
    background: rgba(99,102,241,0.15); color: #818cf8;
    border: 1px solid rgba(99,102,241,0.3); border-radius: 99px;
    font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem;
}
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
                color = "#10b981" if e["final_score"] >= 3.5 else "#f59e0b" if e["final_score"] >= 2.0 else "#ef4444"
                st.markdown(f"""
<div class="score-card">
  <b>{e['skill']}</b> &nbsp;
  <span style="color:{color};font-weight:600">{e['proficiency']}</span>
  <span style="float:right;color:#94a3b8">{e['final_score']:.1f}/5</span>
  <div class="score-bar-container">
    <div class="score-bar" style="width:{pct}%;background:linear-gradient(90deg,{color},{color}aa)"></div>
  </div>
  <small style="color:#94a3b8;font-style:italic">{e['reasoning']}</small>
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
  <p style="color:#94a3b8;font-size:0.9rem">
    50+ skills mapped with relationships. Deterministic gap analysis
    — no LLM hallucinations for skill identification.
  </p>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="score-card">
  <h4>Hybrid Scoring Engine</h4>
  <p style="color:#94a3b8;font-size:0.9rem">
    3-signal evaluation: LLM qualitative score + semantic similarity
    + keyword coverage. Objective and explainable.
  </p>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class="score-card">
  <h4>RAG Resource Curator</h4>
  <p style="color:#94a3b8;font-size:0.9rem">
    Learning plan grounded in 35+ real, curated resources from
    ChromaDB. No hallucinated links — ever.
  </p>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Paste a Job Description and upload your Resume in the sidebar to begin your assessment.")
