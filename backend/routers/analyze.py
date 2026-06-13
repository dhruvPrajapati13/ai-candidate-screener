from fastapi import APIRouter, HTTPException
from models.schemas import AnalyzeRequest, AnalyzeResponse, ScoreBreakdown
from services.gemini_scorer import score_candidate

router = APIRouter()


# ── POST /api/analyze ─────────────────────────────────────
@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_candidate(request: AnalyzeRequest):

    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="resume_text cannot be empty.")

    if not request.transcript.strip():
        raise HTTPException(status_code=400, detail="transcript cannot be empty.")

    try:
        result = score_candidate(request.resume_text, request.transcript)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini scoring failed: {str(e)}")

    return AnalyzeResponse(
        candidate_name   = result.get("candidate_name"),
        summary          = result["summary"],
        strengths        = result["strengths"],
        weaknesses       = result["weaknesses"],
        scores           = ScoreBreakdown(
            technical_skills     = result["scores"]["technical_skills"],
            communication        = result["scores"]["communication"],
            experience_relevance = result["scores"]["experience"],
            project_quality      = result["scores"]["projects"],
            overall              = result["scores"]["overall"],
        ),
        consistency_note = result["consistency_note"],
        recommendation   = result["recommendation"],
    )
