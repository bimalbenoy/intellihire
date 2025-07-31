# app/interface/routes/scoring.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.infrastructure.model.scorer_impl import ScorerImpl

router = APIRouter()

class ScoreRequest(BaseModel):
    resume: str
    job_description: str

# Pydantic models for the detailed response
class ExtractedContentDetail(BaseModel):
    experience: str
    skills: List[str]
    education: str
    years_experience: int
    education_norm: str
    education_fields: List[str]

class ExtractedContentJD(BaseModel):
    experience: str
    skills: List[str]
    education: str
    required_years: int
    education_norm: str
    education_fields: List[str]

class ExtractedContent(BaseModel):
    resume: ExtractedContentDetail
    jd: ExtractedContentJD

class SectionScores(BaseModel):
    experience_score: float
    skill_score: float
    education_score: float
    jaccard_skill_score: float
    semantic_skill_score: float
    years_score: float

class ScoreResponse(BaseModel):
    score: float
    status: str
    section_scores: SectionScores
    extracted_content: ExtractedContent

@router.post("/score", response_model=ScoreResponse)
def score_endpoint(payload: ScoreRequest):
    try:
        scorer = ScorerImpl()
        result = scorer.score(payload.resume, payload.job_description)
        return result
    except Exception as e:
        print(f"Scoring failed with error: {e}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")