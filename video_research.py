
import os
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from faster_whisper import WhisperModel
from ai_model import ask_ai


MAX_VIDEO_BYTES = 100 * 1024 * 1024  # 100 MB
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}

# Downloads the speech model on first use.
# For a laptop with limited memory, start with "small".
_whisper_model = None


def get_whisper_model():
    global _whisper_model

    if _whisper_model is None:
        _whisper_model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    return _whisper_model


def get_youtube_id(url):
    parsed = urlparse(url)

    if parsed.hostname not in {
        "youtube.com", "www.youtube.com", "m.youtube.com",
        "youtu.be", "www.youtube-nocookie.com"
    }:
        raise ValueError("Please provide a valid YouTube URL.")

    if parsed.hostname in {"youtu.be"}:
        video_id = parsed.path.strip("/")
    else:
        video_id = parse_qs(parsed.query).get("v", [""])[0]

        if not video_id and parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/")[2]

    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        raise ValueError("Could not identify the YouTube video.")

    return video_id


def youtube_transcript(url):
    video_id = get_youtube_id(url)

    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)

    lines = []
    for item in transcript:
        start = float(item.start)
        text = item.text.strip()
        timestamp = f"{int(start // 60):02d}:{int(start % 60):02d}"
        lines.append({
            "timestamp": timestamp,
            "seconds": start,
            "text": text
        })

    if not lines:
        raise ValueError("No transcript was available for this video.")

    return lines


def uploaded_video_transcript(file_bytes, filename):
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Supported video formats: MP4, MOV, MKV and WEBM."
        )

    if len(file_bytes) > MAX_VIDEO_BYTES:
        raise ValueError("Video must be 100 MB or smaller.")

    with tempfile.TemporaryDirectory() as temp_dir:
        video_path = Path(temp_dir) / f"input{extension}"

        video_path.write_bytes(file_bytes)

        # Extract audio using FFmpeg.
        audio_path = Path(temp_dir) / "audio.wav"

        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(video_path),
                "-vn", "-ac", "1", "-ar", "16000",
                str(audio_path)
            ],
            check=True,
            capture_output=True,
            timeout=300
        )

        model = get_whisper_model()
        segments, _ = model.transcribe(
            str(audio_path),
            vad_filter=True
        )

        lines = []
        for segment in segments:
            start = float(segment.start)
            timestamp = f"{int(start // 60):02d}:{int(start % 60):02d}"

            lines.append({
                "timestamp": timestamp,
                "seconds": start,
                "text": segment.text.strip()
            })

        if not lines:
            raise ValueError("No speech could be detected in this video.")

        return lines


def analyze_video(lines, source_label):
    transcript = "\n".join(
        f"[{line['timestamp']}] {line['text']}"
        for line in lines
    )

    prompt = f"""
You are the video research assistant for ResearchAI.

Video source: {source_label}

VIDEO TRANSCRIPT WITH TIMESTAMPS:
{transcript}

Create a detailed report with these sections:

1. Video Overview
2. Detailed Summary
3. Important Key Points
4. Timestamped Highlights
5. Main Arguments and Explanations
6. Benefits and Limitations, where relevant
7. Conclusion
8. Further Research Suggestions

Requirements:
- Explain the content clearly and in detail.
- Include relevant timestamps in the format [MM:SS].
- Use only timestamps supplied in the transcript.
- Do not invent video statements, facts or quotations.
- Distinguish what the speaker says from your own analysis.
- The transcript alone does not prove external claims are true.
- Include external source URLs only if they are independently
  available in supplied research data. Never fabricate links.
- If the transcript is incomplete, state that limitation.
- Return a complete, well-structured Markdown report.
"""

    report = ask_ai(prompt)

    return {
        "source": source_label,
        "transcript": transcript,
        "report": report,
        "highlights": lines
    }