from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from routers import upload, analyze


# ── Startup / Shutdown ────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("uploads", exist_ok=True)
    print("✅ Uploads folder ready")
    yield
    # On shutdown (nothing to clean up for now)
    print("👋 Server shutting down")


# ── App Instance ──────────────────────────────────────────
app = FastAPI(
    title="AI Candidate Evaluator",
    description="Analyze resumes and intro videos to score and summarize candidates.",
    version="1.0.0",
    lifespan=lifespan,
)


# ── CORS (allow React frontend on port 5173) ──────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Static Files (serve uploaded files if needed) ─────────
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# ── Routers ───────────────────────────────────────────────
app.include_router(upload.router,  prefix="/api", tags=["Upload"])
app.include_router(analyze.router, prefix="/api", tags=["Analyze"])


# ── Health Check ──────────────────────────────────────────
@app.get("/")
def root():
    return {
        "status": "running",
        "message": "AI Candidate Evaluator API is live.",
        "docs": "/docs",
    }
