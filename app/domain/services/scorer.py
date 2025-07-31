from abc import ABC, abstractmethod

class Scorer(ABC):
    @abstractmethod
    def score(self, resume: str, job_description: str) -> dict:
        """
        Score a resume against a job description.

        Args:
            resume (str): Raw text of the candidate's resume.
            job_description (str): Raw text of the job description.

        Returns:
            dict: {
                "score": float (0-100),
                "status": "Qualified" | "Disqualified",
                "section_scores": {
                    "experience_score": float,
                    "skill_score": float,
                    "education_score": float
                }
            }
        """
        pass