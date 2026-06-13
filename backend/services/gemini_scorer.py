import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ── Configure Gemini ──────────────────────────────────────
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_model = genai.GenerativeModel("models/gemini-2.5-flash")


# ── Main entry point ──────────────────────────────────────
def score_candidate(resume_text: str, transcript: str) -> dict:
    """
    Sends resume text + video transcript to Gemini 2.5 Flash.
    Returns a structured dict with scores, summary, strengths,
    weaknesses, consistency note, and recommendation.
    """
    prompt = _build_prompt(resume_text, transcript)

    response = _model.generate_content(prompt)
    raw      = response.text.strip()

    return _parse_response(raw)


# ── Prompt builder ────────────────────────────────────────
def _build_prompt(resume_text: str, transcript: str) -> str:
    return f"""
You are an expert HR analyst and technical recruiter. You will be given:
1. A candidate's resume text
2. A transcript of the candidate's self-introduction video

Your job is to carefully analyze both and return a structured JSON evaluation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESUME:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{resume_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIDEO TRANSCRIPT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{transcript}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTRUCTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analyze the candidate based on both sources and return ONLY a valid JSON object.
No explanation, no markdown, no code blocks. Just raw JSON.

Score each category from 1 to 10 using these guidelines:
- technical_skills  : Depth and breadth of technical skills mentioned in resume and video
- communication     : Clarity, structure, and confidence in the video transcript
- experience        : Relevance and quality of work experience and internships
- projects          : Complexity, impact, and quality of projects described
- overall           : Your holistic assessment of the candidate

For recommendation use exactly one of: "Strong Hire", "Consider", "Pass"

Return this exact JSON structure:
{{
  "candidate_name": "extracted full name or null",
  "summary": "3-4 sentence overall summary of the candidate",
  "strengths": [
    "specific strength 1",
    "specific strength 2",
    "specific strength 3"
  ],
  "weaknesses": [
    "specific area for improvement 1",
    "specific area for improvement 2"
  ],
  "scores": {{
    "technical_skills": 0,
    "communication": 0,
    "experience": 0,
    "projects": 0,
    "overall": 0
  }},
  "consistency_note": "one sentence about whether what the candidate said in the video matches their resume",
  "recommendation": "Strong Hire | Consider | Pass"
}}
""".strip()


# ── Response parser ───────────────────────────────────────
def _parse_response(raw: str) -> dict:
    """
    Parses Gemini's response into a clean Python dict.
    Handles cases where Gemini wraps output in markdown code fences.
    """
    # Strip markdown code fences if present (```json ... ```)
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$",          "", cleaned, flags=re.MULTILINE)
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Gemini returned invalid JSON.\n"
            f"Error: {e}\n"
            f"Raw response:\n{raw[:500]}"
        )

    # Validate required keys exist
    required = ["candidate_name", "summary", "strengths", "weaknesses",
                "scores", "consistency_note", "recommendation"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Gemini response missing keys: {missing}")

    # Validate scores
    score_keys = ["technical_skills", "communication", "experience", "projects", "overall"]
    for key in score_keys:
        if key not in data["scores"]:
            raise ValueError(f"Missing score key: {key}")
        # Clamp scores to 1-10 range
        data["scores"][key] = max(1, min(10, int(data["scores"][key])))

    # Validate recommendation value
    valid_recommendations = {"Strong Hire", "Consider", "Pass"}
    if data["recommendation"] not in valid_recommendations:
        data["recommendation"] = "Consider"   # safe fallback

    return data
