import pdfplumber
import docx2txt
import re
from pathlib import Path


# ── Main entry point ──────────────────────────────────────
def parse_resume(file_path: str) -> dict:
    """
    Given a path to a PDF or DOCX resume, returns:
    {
        "raw_text": "...",
        "name":     "...",
        "email":    "...",
        "phone":    "...",
        "skills":   [...],
        "education": [...],
        "experience": [...],
    }
    """
    path = Path(file_path)
    ext  = path.suffix.lower()

    if ext == ".pdf":
        raw_text = _extract_pdf(file_path)
    elif ext in (".docx", ".doc"):
        raw_text = _extract_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    if not raw_text.strip():
        raise ValueError("Could not extract any text from the resume file.")

    return {
        "raw_text":   raw_text,
        "name":       _extract_name(raw_text),
        "email":      _extract_email(raw_text),
        "phone":      _extract_phone(raw_text),
        "skills":     _extract_skills(raw_text),
        "education":  _extract_section(raw_text, "education"),
        "experience": _extract_section(raw_text, "experience"),
    }


# ── Text extraction ───────────────────────────────────────
def _extract_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def _extract_docx(file_path: str) -> str:
    return docx2txt.process(file_path).strip()


# ── Entity extraction ─────────────────────────────────────
def _extract_email(text: str) -> str:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else ""


def _extract_phone(text: str) -> str:
    match = re.search(
        r"(\+?\d[\d\s\-\(\)]{8,}\d)", text
    )
    return match.group(0).strip() if match else ""


def _extract_name(text: str) -> str:
    """
    Heuristic: the candidate name is usually the first non-empty
    line of the resume that isn't an email/phone/URL.
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines[:5]:  # check first 5 lines only
        if (
            len(line.split()) <= 6          # names are short
            and not re.search(r"[@/\\|]", line)  # no email/url chars
            and not re.search(r"\d{4}", line)     # no years
            and line[0].isupper()                 # starts with capital
        ):
            return line
    return ""


def _extract_skills(text: str) -> list[str]:
    """
    Finds a Skills section and returns individual skill tokens.
    Falls back to matching against a known skills list.
    """
    # Try to find a skills section block
    section = _extract_section(text, "skills")
    if section:
        # Split by common delimiters
        raw = re.split(r"[,\|•\n]+", section)
        skills = [s.strip() for s in raw if 2 < len(s.strip()) < 40]
        if skills:
            return skills[:30]  # cap at 30

    # Fallback: scan full text for known tech keywords
    known = [
        "Python", "Java", "C++", "C#", "JavaScript", "TypeScript",
        "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin",
        "React", "Angular", "Vue", "Node.js", "FastAPI", "Flask",
        "Django", "Spring", "Express",
        "TensorFlow", "PyTorch", "Keras", "Scikit-Learn",
        "LangChain", "HuggingFace", "OpenCV",
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis",
        "Docker", "Kubernetes", "AWS", "GCP", "Azure",
        "Git", "GitHub", "REST", "GraphQL",
        "Machine Learning", "Deep Learning", "NLP",
        "Generative AI", "LLM", "RAG",
        "Pandas", "NumPy", "Matplotlib",
        "Pinecone", "FAISS", "ChromaDB",
        "Streamlit", "Jupyter",
    ]
    found = [k for k in known if re.search(rf"\b{re.escape(k)}\b", text, re.IGNORECASE)]
    return found


def _extract_section(text: str, section_name: str) -> str:
    """
    Extracts the text block under a given section heading.
    Stops at the next section heading.
    """
    # Common section heading patterns
    headings = [
        "experience", "education", "skills", "projects",
        "certifications", "achievements", "summary",
        "objective", "publications", "awards", "languages",
    ]

    lines   = text.splitlines()
    capture = False
    result  = []

    for line in lines:
        stripped = line.strip()

        # Detect start of our target section
        if re.match(rf"^{section_name}s?\s*$", stripped, re.IGNORECASE) or \
           re.match(rf"^{section_name}s?\s*[:\-]", stripped, re.IGNORECASE):
            capture = True
            continue

        # Detect start of a different section → stop
        if capture:
            is_other_heading = any(
                re.match(rf"^{h}s?\s*[:\-]?\s*$", stripped, re.IGNORECASE)
                for h in headings
                if h != section_name
            )
            if is_other_heading and stripped:
                break
            result.append(line)

    return "\n".join(result).strip()
