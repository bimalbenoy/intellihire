from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.infrastructure.model.scorer_impl import ScorerImpl

router = APIRouter()
scorer = ScorerImpl()

class ScoreRequest(BaseModel):
    resume: str
    job_description: str

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

@router.post("/score", response_model=ScoreResponse)
def score_endpoint(payload: ScoreRequest):
    try:
        result = scorer.score(payload.resume, payload.job_description)
        # Ensure the response only contains fields defined in ScoreResponse
        response_data = {
            "score": result["score"],
            "status": result["status"],
            "section_scores": result["section_scores"]
        }
        return response_data
    except Exception as e:
        print(f"Scoring failed with error: {e}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")