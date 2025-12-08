import os
import time
import random
from fastapi import UploadFile, HTTPException
from dotenv import load_dotenv
from pathlib import Path
from typing import Set

load_dotenv()

ALLOWED_IMAGE_EXT = set(os.getenv("ALLOWED_IMAGE_TYPES", "jpg,jpeg,png,webp").split(","))
ALLOWED_VIDEO_EXT = set(os.getenv("ALLOWED_VIDEO_TYPES", "mp4,mkv,mov,avi").split(","))
ALLOWED_DOC_EXT = set(os.getenv("ALLOWED_DOC_TYPES", "pdf,doc,docx").split(","))

ALLOWED_EXT: Set[str] = ALLOWED_IMAGE_EXT | ALLOWED_VIDEO_EXT | ALLOWED_DOC_EXT


async def validate_file_type(file: UploadFile):
    if not file or not file.filename:
        return

    ext = file.filename.split(".")[-1].lower()

    if ext not in ALLOWED_EXT:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: .{ext}. Allowed: {', '.join(ALLOWED_EXT)}"
        )


async def save_uploaded_file(file: UploadFile, directory: str = "uploads") -> str:
    """Save uploaded file with timestamp + random number."""
    await validate_file_type(file)

    Path(directory).mkdir(parents=True, exist_ok=True)

    ext = file.filename.split(".")[-1].lower()

    # Create unique file name
    timestamp = int(time.time() * 1000)         # milliseconds
    rand = random.randint(1000, 9999)           # 4-digit random number
    new_filename = f"{timestamp}_{rand}.{ext}"

    file_path = os.path.join(directory, new_filename)

    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return file_path
