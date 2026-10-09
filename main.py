from fastapi import FastAPI
from fastapi import UploadFile, File
from photo_search import search_photos
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import threading
import uuid
from datetime import datetime

from orchestrator import run_research
from ai_model import ask_ai
from auth import register_user, login_user
from otp import send_otp, verify_otp
from fastapi import HTTPException
from video_research import (
    youtube_transcript,
    uploaded_video_transcript,
    analyze_video
)

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

class YouTubeVideoRequest(BaseModel):
    url: str

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


@app.get("/search-photos")
def search_photos_api(topic: str):
    topic = topic.strip()

    if not topic:
        return {
            "success": False,
            "photos": [],
            "message": "Please enter a research topic."
        }

    return search_photos(topic)

import base64
from groq import Groq
import os

@app.post("/analyze-photo")
async def analyze_photo(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        return {
            "success": False,
            "message": "Please upload an image."
        }

    image_bytes = await file.read()

    if not image_bytes:
        return {
            "success": False,
            "message": "The uploaded photo is empty."
        }

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this image. Describe what is visible, identify important details, and explain them clearly. Do not guess details that cannot be seen."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{file.content_type};base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=700
        )

        analysis = response.choices[0].message.content

        return {
            "success": True,
            "filename": file.filename,
            "analysis": analysis
        }

    except Exception as e:
        print("Photo Analysis Error:", str(e))
        return {
            "success": False,
            "message": "Unable to analyze this photo. Check the AI model and API settings."
        }
    
# ==========================================
# VIDEO RESEARCH - UPLOAD VIDEO
# ==========================================

@app.post("/research-video/upload")
async def research_uploaded_video(file: UploadFile = File(...)):
    try:
        filename = file.filename or ""
        content = await file.read(100 * 1024 * 1024 + 1)

        if len(content) > 100 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="Video must be 100 MB or smaller."
            )

        lines = uploaded_video_transcript(content, filename)
        return analyze_video(lines, filename)

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print("Video Upload Error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Unable to process video. Check FFmpeg and server logs."
        )


# ==========================================
# VIDEO RESEARCH - YOUTUBE LINK
# ==========================================

@app.post("/research-video/youtube")
def research_youtube_video(request: YouTubeVideoRequest):
    try:
        lines = youtube_transcript(request.url)
        return analyze_video(lines, request.url)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print("YouTube Research Error:", repr(e))
        raise HTTPException(
            status_code=422,
            detail="Transcript unavailable. Check the YouTube captions or server logs."
        )