import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import ResumeUploadResponse, VideoUploadResponse
from services.resume_parser import parse_resume
from services.video_transcriber import transcribe_video

router = APIRouter()

UPLOAD_DIR     = "uploads"
ALLOWED_RESUME = {".pdf", ".docx", ".doc"}
ALLOWED_VIDEO  = {".mp4", ".mov", ".webm", ".avi"}


# ── POST /api/upload/resume ───────────────────────────────
@router.post("/upload/resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_RESUME:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{ext}'. Allowed: {ALLOWED_RESUME}"
        )

    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path   = os.path.join(UPLOAD_DIR, unique_name)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        parsed = parse_resume(save_path)
    except Exception as e:
        os.remove(save_path)
        raise HTTPException(status_code=422, detail=f"Resume parsing failed: {str(e)}")

    return ResumeUploadResponse(
        message     = "Resume uploaded and parsed successfully.",
        filename    = file.filename,
        resume_text = parsed["raw_text"],
        name        = parsed["name"],
        email       = parsed["email"],
        skills      = parsed["skills"],
    )


# ── POST /api/upload/video ────────────────────────────────
@router.post("/upload/video", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_VIDEO:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{ext}'. Allowed: {ALLOWED_VIDEO}"
        )

    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path   = os.path.join(UPLOAD_DIR, unique_name)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        transcript = transcribe_video(save_path)
    except Exception as e:
        os.remove(save_path)
        raise HTTPException(status_code=422, detail=f"Video transcription failed: {str(e)}")

    if not transcript.strip():
        raise HTTPException(
            status_code=422,
            detail="Transcription produced no text. Check that the video has clear audio."
        )

    return VideoUploadResponse(
        message    = "Video uploaded and transcribed successfully.",
        filename   = file.filename,
        video_path = save_path,
        transcript = transcript,
    )
