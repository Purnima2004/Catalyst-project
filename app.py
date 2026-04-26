import streamlit as st
import os
import uuid
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# We only import the graph and utilities after loading dotenv so API keys are available
from utils.pdf_parser import extract_text_from_pdf
from agent.graph import graph

# Set up page
st.set_page_config(page_title="Catalyst | Skill Assessment", page_icon="🚀", layout="wide")

# Custom CSS for a premium look
st.markdown("""
<style>
    :root {
        --primary: #6366f1;
        --background: #0f172a;
        --surface: #1e293b;
        --text: #f8fafc;
    }
    
    .stApp {
        background-color: var(--background);
        color: var(--text);
    }
    
    .stSidebar {
        background-color: var(--surface) !important;
    }
    
    h1, h2, h3 {
        color: var(--text) !important;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        color: white;
    }
    
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.7);
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    
    .stChatInputContainer {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Catalyst AI Skill Assessor")
st.markdown("A dynamic agent that evaluates real proficiency and builds personalized learning plans.")

# Initialize session state for thread_id and config
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.config = {"configurable": {"thread_id": st.session_state.thread_id}}

config = st.session_state.config

# Sidebar for inputs
with st.sidebar:
    st.header("Candidate Information")
    job_description = st.text_area("Job Description", height=200, placeholder="Paste the JD here...")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    
    start_interview = st.button("Start Assessment", type="primary", use_container_width=True)

if start_interview and job_description and resume_file:
    with st.spinner("Analyzing profile and identifying core skills..."):
        resume_text = extract_text_from_pdf(resume_file.read())
        initial_state = {
            "job_description": job_description,
            "resume_text": resume_text,
            "messages": []
        }
        # Start graph execution
        graph.invoke(initial_state, config)
        st.session_state.started = True

if st.session_state.get("started", False):
    # Fetch current state from LangGraph
    state = graph.get_state(config)
    
    # Determine if graph has finished (no next node)
    if not state.next:
        st.success("✨ Assessment Complete!")
        st.markdown("### 🎯 Your Personalized Learning Plan")
        plan = state.values.get("learning_plan", "")
        st.markdown(plan)
        
        with st.expander("View Detailed Evaluations"):
            evals = state.values.get("evaluations", [])
            for e in evals:
                st.write(f"**{e['skill']}**: {e['proficiency']} ({e['score']}/5)")
                st.write(f"_{e['reasoning']}_")
                st.divider()
    else:
        # We are paused at the 'human' node
        messages = state.values.get("messages", [])
        
        # Display chat history
        for msg in messages:
            if isinstance(msg, AIMessage):
                with st.chat_message("assistant"):
                    st.write(msg.content)
            elif isinstance(msg, HumanMessage):
                with st.chat_message("user"):
                    st.write(msg.content)
        
        # Chat input
        user_input = st.chat_input("Your answer...")
        if user_input:
            with st.chat_message("user"):
                st.write(user_input)
            
            with st.spinner("Evaluating response..."):
                # Update state with the user's answer, acting as the 'human' node
                graph.update_state(config, {"messages": [HumanMessage(content=user_input)]}, as_node="human")
                # Resume graph
                graph.invoke(None, config)
            
            # Rerun to update chat with next question or final plan
            st.rerun()
elif not st.session_state.get("started", False):
    st.info("👈 Please paste a Job Description and upload a Resume in the sidebar to begin.")
