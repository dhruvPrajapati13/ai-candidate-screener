# AI Candidate Screener

## Overview

AI Candidate Screener is a full-stack AI-powered recruitment assistant that evaluates candidates by analyzing both their resume and self-introduction video.

The system extracts information from resumes (PDF/DOCX), transcribes candidate introduction videos, and uses Google's Gemini AI to generate candidate assessments, score breakdowns, strengths, weaknesses, consistency analysis, and hiring recommendations.

---

## Features

* Resume Upload (PDF, DOC, DOCX)
* Resume Text Extraction and Parsing
* Candidate Information Extraction

  * Name
  * Email
  * Phone Number
  * Skills
  * Education
  * Experience
* Video Upload (MP4, MOV, WebM, AVI)
* Automatic Audio Extraction using FFmpeg
* Video Transcription using Hinglish Speech-to-Text Model
* AI-Powered Candidate Evaluation using Gemini
* Technical Skill Assessment
* Communication Assessment
* Experience Relevance Scoring
* Project Quality Evaluation
* Resume vs Video Consistency Analysis
* Hiring Recommendation Generation
* Interactive Dashboard with Score Visualization

---

## System Architecture

```text
Resume Upload
      │
      ▼
Resume Parser
      │
      ▼
Resume Text

Video Upload
      │
      ▼
FFmpeg Audio Extraction
      │
      ▼
Speech-to-Text Transcription
      │
      ▼
Transcript

Resume Text + Transcript
      │
      ▼
Gemini AI Evaluation
      │
      ▼
Candidate Report
```

---

## Tech Stack

### Backend

* FastAPI
* Python
* Pydantic
* Uvicorn
* Python Multipart

### AI & Machine Learning

* Google Gemini 2.5 Flash
* Transformers
* PyTorch
* Hugging Face Pipelines

### Resume Processing

* pdfplumber
* python-docx
* docx2txt

### Video Processing

* FFmpeg
* Speech Recognition Pipeline

### Frontend

* HTML5
* CSS3
* JavaScript (Vanilla JS)

---

## Project Structure

```text
AI-Candidate-Screener
│
├── backend
│   ├── models
│   ├── routers
│   ├── services
│   ├── main.py
│   ├── requirements.txt
│   └── test.py
│
├── frontend
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── schemas.py
```

---

## API Endpoints

### Upload Resume

```http
POST /api/upload/resume
```

Uploads and parses a candidate resume.

### Upload Video

```http
POST /api/upload/video
```

Uploads and transcribes a candidate introduction video.

### Analyze Candidate

```http
POST /api/analyze
```

Generates AI-powered candidate evaluation.

### Health Check

```http
GET /
```

Returns API status.

---

## Scoring Categories

Candidates are evaluated on a scale of 1–10 in the following areas:

| Category         | Description                             |
| ---------------- | --------------------------------------- |
| Technical Skills | Technical expertise and skill depth     |
| Communication    | Clarity and confidence in communication |
| Experience       | Relevance of work experience            |
| Projects         | Quality and impact of projects          |
| Overall          | Overall candidate assessment            |

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/dhruvPrajapati13/ai-candidate-screener.git
cd ai-candidate-screener
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the backend folder:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

### 5. Start Backend

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start Frontend

```bash
cd frontend
python3 -m http.server 5500
```

Open:

```text
http://localhost:5500
```

---

## Workflow

1. Upload candidate resume.
2. Upload candidate introduction video.
3. Resume text is extracted and parsed.
4. Video audio is extracted using FFmpeg.
5. Speech-to-text model generates transcript.
6. Resume and transcript are sent to Gemini AI.
7. AI generates:

   * Candidate Summary
   * Strengths
   * Areas for Improvement
   * Score Breakdown
   * Consistency Analysis
   * Hiring Recommendation

---

## Future Improvements

* Multi-language transcription support
* ATS score generation
* Recruiter dashboard
* Candidate ranking system
* Batch candidate processing
* Interview question generation
* Database integration
* Cloud deployment

---

## Author

**Dhruv Prajapati**

AI & Machine Learning Developer

GitHub: https://github.com/dhruvPrajapati13
