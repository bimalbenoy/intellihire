# app/infrastructure/model/scorer_impl.py

from app.core.text_utils import score_applicant
from typing import Dict, Any

class ScorerImpl:
    def score(self, resume: str, job_description: str) -> Dict[str, Any]:
        return score_applicant(resume, job_description)