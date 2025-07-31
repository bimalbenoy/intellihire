from app.core.text_utils import (
    split_resume_sections,
    split_jd_sections,
    extract_skills,
    jaccard_similarity,
    match_education,
    embed_text,
    extract_years
)

class ScorerImpl:
    def score(self, resume: str, job_description: str) -> dict:
        # Extract structured sections
        resume_sections = split_resume_sections(resume)
        jd_sections = split_jd_sections(job_description)

        # Extract experience texts
        resume_exp = resume_sections.get("experience", "")
        jd_exp = jd_sections.get("experience", "")

        # Experience score: SBERT semantic + years comparison
        semantic_score = embed_text(resume_exp, jd_exp)
        resume_years = extract_years(resume_exp)
        jd_years = extract_years(jd_exp)

        if jd_years == 0:
            year_score = 1.0
        elif resume_years >= jd_years:
            year_score = 1.0
        else:
            year_score = resume_years / jd_years

        experience_score = round((0.7 * semantic_score + 0.3 * year_score), 2)

        # Skill score: Jaccard similarity
        resume_skills = extract_skills(resume_sections.get("skills", ""))
        jd_skills = extract_skills(jd_sections.get("skills", ""))
        skill_score = round(jaccard_similarity(resume_skills, jd_skills), 2)

        # Education score: degree + field match
        resume_edu = resume_sections.get("education", "")
        jd_edu = jd_sections.get("education", "")
        education_score = round(match_education(resume_edu, jd_edu), 2)

        # Weighted scoring
        final_score = 0.5 * experience_score + 0.4 * skill_score + 0.1 * education_score
        final_percentage = round(final_score * 100, 2)

        # Qualification status
        status = "Qualified" if final_percentage >= 60 else "Disqualified"

        return {
            "score": final_percentage,
            "status": status,
            "section_scores": {
                "experience_score": experience_score,
                "skill_score": skill_score,
                "education_score": education_score
            }
        }
