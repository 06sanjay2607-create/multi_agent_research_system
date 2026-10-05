from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import threading
import uuid
from datetime import datetime

from orchestrator import run_research
from auth import register_user, login_user
from otp import send_otp, verify_otp


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Multi-Agent Autonomous Research System"
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# =========================================================
# REQUEST MODELS
# =========================================================

class ResearchRequest(BaseModel):

    topic: str

    document_text: str | None = None

    document_name: str | None = None


class RegisterRequest(BaseModel):

    name: str

    email: str

    password: str


class LoginRequest(BaseModel):

    email: str

    password: str


class OTPRequest(BaseModel):

    email: str

    otp: str | None = None


# =========================================================
# AUTHENTICATION
# =========================================================

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


# =========================================================
# OTP
# =========================================================

@app.post("/send-otp")
def send_otp_api(request: OTPRequest):

    try:

        send_otp(request.email)

        return {
            "success": True,
            "message": "OTP sent successfully"
        }

    except Exception as e:

        print(
            "OTP Send Error:",
            str(e)
        )

        return {
            "success": False,
            "message": "Unable to send OTP."
        }


@app.post("/verify-otp")
def verify_otp_api(request: OTPRequest):

    try:

        if not request.otp:

            return {
                "success": False,
                "message": "OTP is required"
            }

        verified = verify_otp(
            request.email,
            request.otp
        )

        if verified:

            return {
                "success": True,
                "message": "OTP verified successfully"
            }

        return {
            "success": False,
            "message": "Invalid OTP"
        }

    except Exception as e:

        print(
            "OTP Verify Error:",
            str(e)
        )

        return {
            "success": False,
            "message": "Unable to verify OTP."
        }


# =========================================================
# RESEARCH STORAGE
# =========================================================

jobs = {}

history = []


# =========================================================
# RESEARCH JOB
# =========================================================

def run_job(
    job_id,
    topic,
    document_text=None,
    document_name=None
):

    def progress_callback(step, status):

        jobs[job_id]["step"] = step

        jobs[job_id]["status"] = status


    jobs[job_id] = {

        "step": 0,

        "status": "Starting...",

        "report": None,

        "analysis": None,

        "sources": [],

        "facts": [],

        "completed": False

    }


    try:

        result = run_research(
            topic,
            progress_callback=progress_callback,
            document_text=document_text,
            document_name=document_name
        )


        # =================================================
        # STRUCTURED RESULT FROM ORCHESTRATOR
        # =================================================

        if isinstance(result, dict):

            final_report = result.get(
                "report",
                ""
            )

            analysis = result.get(
                "analysis",
                ""
            )

            sources = result.get(
                "sources",
                []
            )

            facts = result.get(
                "facts",
                []
            )

        else:

            final_report = result

            analysis = ""

            sources = []

            facts = []


        # =================================================
        # STORE RESULT
        # =================================================

        jobs[job_id]["report"] = final_report

        jobs[job_id]["analysis"] = analysis

        jobs[job_id]["sources"] = sources

        jobs[job_id]["facts"] = facts

        jobs[job_id]["completed"] = True

        jobs[job_id]["status"] = "Completed"


        # =================================================
        # SAVE HISTORY
        # =================================================

        history.append({

            "job_id": job_id,

            "topic": topic,

            "report": final_report,

            "analysis": analysis,

            "sources": sources,

            "facts": facts,

            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        })


    except Exception as e:

        print(
            "Research Error:",
            str(e)
        )

        jobs[job_id]["status"] = "Error"

        jobs[job_id]["report"] = str(e)

        jobs[job_id]["analysis"] = ""

        jobs[job_id]["sources"] = []

        jobs[job_id]["completed"] = False


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/")
def home():

    return FileResponse(
        "static/index.html"
    )


# =========================================================
# START RESEARCH
# =========================================================

@app.post("/research")
def research(request: ResearchRequest):

    job_id = str(
        uuid.uuid4()
    )


    thread = threading.Thread(

        target=run_job,

        args=(
            job_id,
            request.topic,
            request.document_text,
            request.document_name
        )

    )


    thread.start()


    return {

        "job_id": job_id

    }


# =========================================================
# RESEARCH STATUS
# =========================================================

@app.get("/research/{job_id}/status")
def research_status(job_id: str):

    if job_id not in jobs:

        return {

            "error": "Job not found"

        }


    job = jobs[job_id]


    return {

        "step": job.get(
            "step",
            0
        ),

        "status": job.get(
            "status",
            ""
        ),

        "report": job.get(
            "report",
            ""
        ),

        "analysis": job.get(
            "analysis",
            ""
        ),

        "sources": job.get(
            "sources",
            []
        ),

        "facts": job.get(
            "facts",
            []
        ),

        "completed": job.get(
            "completed",
            False
        )

    }


# =========================================================
# RESEARCH HISTORY
# =========================================================

@app.get("/history")
def get_history():

    return {

        "history": history

    }


# =========================================================
# DOCUMENT UPLOAD
# =========================================================

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...)
):

    try:

        content = await file.read()

        filename = file.filename.lower()


        # =================================================
        # PDF
        # =================================================

        if filename.endswith(".pdf"):

            from io import BytesIO
            from pypdf import PdfReader


            reader = PdfReader(
                BytesIO(content)
            )


            text = ""


            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"


        # =================================================
        # DOCX
        # =================================================

        elif filename.endswith(".docx"):

            from io import BytesIO
            from docx import Document


            document = Document(
                BytesIO(content)
            )


            text = "\n".join(

                paragraph.text

                for paragraph in document.paragraphs

            )


        # =================================================
        # TXT
        # =================================================

        elif filename.endswith(".txt"):

            text = content.decode(
                "utf-8",
                errors="ignore"
            )


        # =================================================
        # UNSUPPORTED FILE
        # =================================================

        else:

            return {

                "success": False,

                "message":
                "Only PDF, DOCX and TXT files are supported."

            }


        return {

            "success": True,

            "filename": file.filename,

            "message":
            "Document uploaded successfully",

            "text": text

        }


    except Exception as e:

        print(
            "Document Upload Error:",
            str(e)
        )


        return {

            "success": False,

            "message":
            "Unable to process document."

        }