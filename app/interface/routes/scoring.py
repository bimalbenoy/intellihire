from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.infrastructure.model.scorer_impl import ScorerImpl

router = APIRouter()

class ScoreRequest(BaseModel):
    resume: str
    job_description: str

class ScoreResponse(BaseModel):
    score: float
    status: str
    section_scores: dict

@router.post("/score", response_model=ScoreResponse)
def score_endpoint(payload: ScoreRequest):
    try:
        scorer = ScorerImpl()
        result = scorer.score(payload.resume, payload.job_description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")
