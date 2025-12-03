from fastapi import APIRouter, HTTPException
from faster_whisper import WhisperModel
import requests
import uuid
import os
import traceback
from pydantic import BaseModel

class VideoRequest(BaseModel):
    video_url: str

router = APIRouter(prefix="/transcript", tags=["Transcript"])


def download_video(url: str) -> str:
    filename = f"temp_{uuid.uuid4()}.mp4"
    r = requests.get(url, stream=True)

    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download video")

    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    return filename


@router.post("/generate")
def generate_transcript(body: VideoRequest):
    print("API CALLED")  # debug print

    video_url = body.video_url
    print("Video URL:", video_url)

    try:
        video_path = download_video(video_url)
        print("Video downloaded to:", video_path)
    except Exception as e:
        print("Download error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

    try:
        print("Loading Whisper model...")
        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="float32"
        )
        print("Model loaded successfully.")
    except Exception as e:
        print("MODEL LOAD ERROR:\n", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Whisper model load failed: " + str(e))

    try:
        print("Starting transcription...")
        segments, info = model.transcribe(video_path)
        print("Transcription completed.")
    except Exception as e:
        print("TRANSCRIPTION ERROR:\n", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Transcription failed: " + str(e))

    transcript_list = []
    full_text = ""

    try:
        for seg in segments:
            print("Segment:", seg.text)
            transcript_list.append({
                "start": seg.start,
                "end": seg.end,
                "text": seg.text
            })
            full_text += seg.text + " "
    except Exception as e:
        print("SEGMENT PARSE ERROR:\n", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Segment parse error: " + str(e))

    print("Sending Response...")
    return {
        "success": True,
        "transcript": full_text.strip(),
        "segments": transcript_list
    }