from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from main import run_university_ranking, run_pyq_retrieval
from ingestion.syllabus_fetcher import fetch_syllabus, TRUSTED_SOURCES

from fastapi.middleware.cors import CORSMiddleware


# ✅ Create app FIRST
app = FastAPI(title="Academic Intelligence API")

# ✅ Then add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Schemas ----------

class InterestRequest(BaseModel):
    interest: str


class PyqRequest(BaseModel):
    interest: str
    entrance: str
    subject: str


class RefreshRequest(BaseModel):
    source_key: str


# ---------- Endpoints ----------

@app.post("/rank-universities")
def rank_universities(req: InterestRequest):
    return run_university_ranking(req.interest)


@app.post("/get-pyqs")
def get_pyqs(req: PyqRequest):
    pyqs = run_pyq_retrieval(
        entrance=req.entrance,
        subject=req.subject,
        interest_text=req.interest
    )
    return {"pyqs": pyqs}


@app.post("/refresh-syllabus")
def refresh_syllabus(req: RefreshRequest):
    result = fetch_syllabus(req.source_key)
    return result


@app.get("/available-sources")
def available_sources():
    return {"sources": list(TRUSTED_SOURCES.keys())}