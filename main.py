from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import threading
import uuid
from datetime import datetime

from orchestrator import run_research 
from auth import register_user, login_user


app = FastAPI(title="Multi-Agent Autonomous Research System")


class ResearchRequest(BaseModel):
    topic: str
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/register")
def register(request: RegisterRequest):

    return register_user(
        request.name,
        request.email,
        request.password
    )


@app.post("/login")
def login(request: LoginRequest):

    return login_user(
        request.email,
        request.password
    )

jobs = {}
history = []


def run_job(job_id, topic):

    def progress_callback(step, status):
        jobs[job_id]["step"] = step
        jobs[job_id]["status"] = status

    jobs[job_id] = {
        "step": 0,
        "status": "Starting...",
        "report": None,
        "completed": False
    }

    try:
        report = run_research(
            topic,
            progress_callback=progress_callback
        )

        jobs[job_id]["report"] = report
        jobs[job_id]["completed"] = True
        jobs[job_id]["status"] = "Completed"

        history.append({
    "job_id": job_id,
    "topic": topic,
    "report": report,
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

    except Exception as e:

        jobs[job_id]["status"] = "Error"
        jobs[job_id]["report"] = str(e)


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/research")
def research(request: ResearchRequest):

    job_id = str(uuid.uuid4())

    thread = threading.Thread(
        target=run_job,
        args=(job_id, request.topic)
    )

    thread.start()

    return {
        "job_id": job_id
    }


@app.get("/research/{job_id}/status")
def research_status(job_id: str):

    if job_id not in jobs:
        return {
            "error": "Job not found"
        }

    return jobs[job_id]

@app.get("/history")
def get_history():

    return {
        "history": history
    }