from pydantic import BaseModel
from typing import Optional


# ── Upload Responses ──────────────────────────────────────

class ResumeUploadResponse(BaseModel):
    message: str
    filename: str
    resume_text: str
    name: Optional[str]
    email: Optional[str]
    skills: list[str]


class VideoUploadResponse(BaseModel):
    message: str
    filename: str
    video_path: str
    transcript: str


# ── Analyze ───────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    resume_text: str
    transcript: str


class ScoreBreakdown(BaseModel):
    technical_skills: int        # 1-10
    communication: int           # 1-10
    experience_relevance: int    # 1-10
    project_quality: int         # 1-10
    overall: int                 # 1-10


class AnalyzeResponse(BaseModel):
    candidate_name: Optional[str]
    summary: str
    strengths: list[str]
    weaknesses: list[str]
    scores: ScoreBreakdown
    consistency_note: str        # resume vs video match observation
    recommendation: str          # "Strong Hire" / "Consider" / "Pass"



