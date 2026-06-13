# AI Candidate Screener

## About the Project

AI Candidate Screener is a web application that helps evaluate job candidates using their resume and introduction video.

The system extracts information from resumes, transcribes the candidate's video, and uses Google's Gemini AI to generate scores, strengths, weaknesses, and a hiring recommendation.

---

## Features

* Upload Resume (PDF/DOCX)
* Upload Introduction Video
* Resume Text Extraction
* Video Transcription
* AI-Based Candidate Evaluation
* Technical Skill Assessment
* Communication Skill Assessment
* Overall Candidate Score
* Hiring Recommendation

---

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic

### AI & ML

* Google Gemini API
* Transformers
* PyTorch

### Resume Processing

* pdfplumber
* docx2txt

### Frontend

* HTML
* CSS
* JavaScript

### Video Processing

* FFmpeg

---

## Project Structure

```text
AI-Candidate-Screener
│
├── backend
│   ├── routers
│   ├── services
│   ├── models
│   ├── main.py
│   └── requirements.txt
│
├── frontend
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── schemas.py
```

---

## How It Works

1. User uploads a resume.
2. User uploads an introduction video.
3. Resume information is extracted.
4. Video audio is converted into text.
5. Resume and transcript are analyzed using Gemini AI.
6. The system generates:

   * Candidate Summary
   * Strengths
   * Weaknesses
   * Score Breakdown
   * Hiring Recommendation

---

## Installation

Clone the repository:

```bash
git clone https://github.com/dhruvPrajapati13/ai-candidate-screener.git
```

Go to backend folder:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the backend:

```bash
uvicorn main:app --reload
```

Run frontend:

```bash
cd frontend
python3 -m http.server 5500
```

Open:

```text
http://localhost:5500
```

---

## Future Improvements

* ATS Score Calculation
* Candidate Ranking
* Interview Question Generation
* Database Integration
* Cloud Deployment

---

## Author

Dhruv Prajapati

GitHub: https://github.com/dhruvPrajapati13
