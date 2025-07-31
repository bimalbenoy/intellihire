from app.infrastructure.model.scorer_impl import ScorerImpl

def score_resume(resume: str, jd: str) -> dict:
    """
    Coordinates resume scoring by invoking the scorer implementation.

    Args:
        resume (str): The raw text of the candidate's resume.
        jd (str): The raw text of the job description.

    Returns:
        dict: A dictionary containing the final score and section-wise scores.
    """
    scorer = ScorerImpl()
    return scorer.score(resume, jd)