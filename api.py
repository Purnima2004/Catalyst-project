from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import os
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage
from utils.pdf_parser import extract_text_from_pdf
from data.candidate_store import hash_bytes, get_candidate, save_candidate
from agents.supervisor import graph

load_dotenv()

app = FastAPI(title="Catalyst AI API")

# Allow requests from our React frontend (running on port 5173 typically)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class StartRequest(BaseModel):
    job_description: str
    resume_hash: str
    resume_text: str
    is_returning_user: bool

class ChatRequest(BaseModel):
    thread_id: str
    message: str

def parse_messages(messages):
    parsed = []
    for msg in messages:
        if isinstance(msg, AIMessage):
            parsed.append({"role": "assistant", "content": msg.content})
        elif isinstance(msg, HumanMessage):
            parsed.append({"role": "user", "content": msg.content})
    return parsed

@app.post("/api/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    pdf_bytes = await file.read()
    resume_hash = hash_bytes(pdf_bytes)
    cached = get_candidate(resume_hash)

    if cached:
        return {
            "is_returning_user": True,
            "resume_hash": resume_hash,
            "resume_text": cached["resume_text"]
        }
    else:
        resume_text = extract_text_from_pdf(pdf_bytes)
        save_candidate(resume_hash, resume_text)
        return {
            "is_returning_user": False,
            "resume_hash": resume_hash,
            "resume_text": resume_text
        }

@app.post("/api/start")
async def start_assessment(req: StartRequest):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "job_description": req.job_description,
        "resume_text": req.resume_text,
        "resume_hash": req.resume_hash,
        "is_returning_user": req.is_returning_user,
        "messages": [],
        "evaluations": [],
    }
    
    # Initialize graph
    graph.invoke(initial_state, config)
    state = graph.get_state(config)
    
    return get_current_state(state, thread_id)

@app.post("/api/chat")
async def chat(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    state = graph.get_state(config)
    
    if not state.next:
        return {"status": "complete", "message": "Assessment is already complete."}

    # Add user message and continue graph execution
    graph.update_state(
        config,
        {"messages": [HumanMessage(content=req.message)]},
        as_node="human"
    )
    graph.invoke(None, config)
    
    new_state = graph.get_state(config)
    return get_current_state(new_state, req.thread_id)

@app.get("/api/state/{thread_id}")
async def get_state(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config)
    return get_current_state(state, thread_id)

def get_current_state(state, thread_id):
    if not state:
        raise HTTPException(status_code=404, detail="Thread not found")
        
    is_complete = not state.next
    values = state.values
    
    return {
        "thread_id": thread_id,
        "is_complete": is_complete,
        "messages": parse_messages(values.get("messages", [])),
        "current_skill_index": values.get("current_skill_index", 0),
        "skills_to_assess": values.get("skills_to_assess", []),
        "evaluations": values.get("evaluations", []),
        "learning_plan": values.get("learning_plan", "")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
