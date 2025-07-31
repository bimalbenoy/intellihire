import re
from sentence_transformers import SentenceTransformer, util
from typing import Dict, Set, List, Any

DEGREE_EQUIVALENTS: Dict[str, str] = {
    "btech": "bachelor", "b.tech": "bachelor", "bachelors": "bachelor", "b.sc": "bachelor", "bs": "bachelor",
    "mtech": "master", "m.tech": "master", "masters": "master", "m.sc": "master", "ms": "master",
    "phd": "doctorate", "doctorate": "doctorate"
}

sbert_model = SentenceTransformer('all-MiniLM-L6-v2') # Load SBERT model globally

def clean(text: str) -> str:
    """Cleans text by converting to lowercase and removing non-alphanumeric characters."""
    if not isinstance(text, str): return ""
    return re.sub(r'[^a-zA-Z0-9 ]', '', text.lower())

def normalize_line(line: str) -> str:
    """Normalizes a single line for header matching."""
    if not isinstance(line, str): return ""
    return re.sub(r'[^a-z]', '', line.strip().lower())

def extract_skills(text: str) -> Set[str]:
    """Extracts a set of normalized skills."""
    if not isinstance(text, str): return set()
    skills_list = re.split(r'[,;\n•\-=*]', text)
    return {skill.strip().lower() for skill in skills_list if skill.strip()}

def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculates Jaccard similarity between two sets."""
    if not set1 or not set2: return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def embed_text(text1: str, text2: str) -> float:
    """Calculates cosine similarity between text embeddings."""
    if not text1 or not text2: return 0.0
    emb1 = sbert_model.encode(text1, convert_to_tensor=True)
    emb2 = sbert_model.encode(text2, convert_to_tensor=True)
    return float(util.cos_sim(emb1, emb2).item())

def split_sections(text: str) -> Dict[str, str]:
    """Splits text into experience, skills, and education sections with fallbacks."""
    sections: Dict[str, str] = {"experience": "", "skills": "", "education": ""}
    current_section: str = None
    lines = text.splitlines()
    temp_sections: Dict[str, List[str]] = {"experience": [], "skills": [], "education": []}

    for line in lines:
        norm_line = normalize_line(line)
        if any(kw in norm_line for kw in ["experience", "work", "employment"]):
            current_section = "experience"
        elif any(kw in norm_line for kw in ["skill", "technologies", "tools", "competencies"]):
            current_section = "skills"
        elif any(kw in norm_line for kw in ["education", "qualification", "degree", "academic"]):
            current_section = "education"
        elif current_section:
            temp_sections[current_section].append(line)

    for sec_name, sec_lines in temp_sections.items():
        sections[sec_name] = "\n".join(sec_lines).strip()

    if not sections["education"]:
        education_keywords_regex = r"(btech|b\.tech|bachelor|degree|master|phd|university|college|school|academic|institute)"
        education_lines = [line for line in lines if re.search(education_keywords_regex, line.lower())]
        if education_lines: sections["education"] = "\n".join(education_lines).strip()

    if not sections["experience"]:
        experience_fallback_keywords = ["years", "backend", "frontend", "fullstack", "django", "rest", "develop", "engineer", "developed", "built", "managed", "led", "contributed", "architected", "implemented", "designed", "created", "maintained"]
        experience_lines = [line for line in lines if any(kw in line.lower() for kw in experience_fallback_keywords)]
        if experience_lines: sections["experience"] = "\n".join(experience_lines).strip()

    if not sections["skills"]:
        skills_fallback_keywords = ["python", "docker", "aws", "ci/cd", "git", "rest", "javascript", "java", "sql", "linux", "api", "database", "cloud", "agile", "microservices", "kubernetes", "html", "css", "react", "angular", "vue", "node", "php", "c++", "c#", "azure", "gcp", "data science", "machine learning", "nlp", "tableau", "excel", "powerbi", "salesforce"]
        skills_lines = [line for line in lines if any(kw in line.lower() for kw in skills_fallback_keywords)]
        if skills_lines: sections["skills"] = "\n".join(skills_lines).strip()

    return sections

def split_resume_sections(text: str) -> Dict[str, str]:
    """Wrapper for splitting resume text."""
    return split_sections(text)

def split_jd_sections(text: str) -> Dict[str, str]:
    """Wrapper for splitting job description text."""
    return split_sections(text)

def normalize_degrees(text: str) -> str:
    """Normalizes degree variations while preserving other content."""
    cleaned_text = clean(text)
    if not cleaned_text: return ""
    normalized_text = cleaned_text
    for variant, standard in DEGREE_EQUIVALENTS.items():
        normalized_text = re.sub(r'\b' + re.escape(variant) + r'\b', standard, normalized_text)
    return normalized_text

def extract_field_keywords(text: str) -> Set[str]:
    """Extracts potential field/major keywords from education text."""
    if not isinstance(text, str): return set()
    field_patterns = [
        r'\b(computer science|cs|computing|comp sci)\b', r'\b(software engineering|software dev|software development)\b',
        r'\b(information technology|it|information systems|is)\b', r'\b(electrical engineering|electronics|ece|ee)\b',
        r'\b(mechanical engineering|mechanical|mech eng)\b', r'\b(civil engineering|civil eng)\b',
        r'\b(chemical engineering|chem eng)\b', r'\b(biomedical engineering|bioeng)\b',
        r'\b(data science|data analytics|data analysis)\b', r'\b(machine learning|artificial intelligence|ai|ml)\b',
        r'\b(business|management|mba|commerce)\b', r'\b(finance|accounting|economics|econ)\b',
        r'\b(marketing|communications|media)\b', r'\b(psychology|sociology|humanities)\b',
        r'\b(biology|chemistry|physics|sciences)\b', r'\b(mathematics|statistics|math)\b',
        r'\b(engineering)\b', r'\b(design|architecture)\b', r'\b(health|nursing|medicine)\b',
        r'\b(arts|liberal arts)\b', r'\b(journalism)\b', r'\b(education)\b'
    ]
    text_lower = text.lower()
    found_fields = set()
    for pattern in field_patterns:
        matches = re.findall(pattern, text_lower)
        for match_group in matches:
            found_fields.add(match_group[0] if isinstance(match_group, tuple) else match_group)
    return found_fields

def semantic_field_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculates semantic similarity between sets of field keywords."""
    if not set1 or not set2: return 0.0
    text1 = " ".join(sorted(list(set1)))
    text2 = " ".join(sorted(list(set2)))
    return embed_text(text1, text2)

def match_education(resume_edu: str, jd_edu: str) -> float:
    """Compares education sections for degree and field matches."""
    resume_edu_norm = normalize_degrees(resume_edu)
    jd_edu_norm = normalize_degrees(jd_edu)
    if not resume_edu_norm or not jd_edu_norm: return 0.0

    degree_match = False
    for standard_degree in set(DEGREE_EQUIVALENTS.values()):
        if standard_degree in resume_edu_norm and standard_degree in jd_edu_norm:
            degree_match = True; break

    resume_fields = extract_field_keywords(resume_edu_norm)
    jd_fields = extract_field_keywords(jd_edu_norm)
    field_sim_score = 0.0

    if resume_fields and jd_fields:
        exact_field_sim = jaccard_similarity(resume_fields, jd_fields)
        semantic_field_sim = semantic_field_similarity(resume_fields, jd_fields)
        field_sim_score = min(0.7 * exact_field_sim + 0.3 * semantic_field_sim, 1.0)
    else:
        field_sim_score = embed_text(resume_edu_norm, jd_edu_norm)

    if degree_match and field_sim_score >= 0.7: return 1.0
    elif degree_match and field_sim_score >= 0.4: return 0.8
    elif degree_match: return 0.6
    elif field_sim_score >= 0.7: return 0.7
    elif field_sim_score >= 0.4: return 0.4
    else: return 0.0

def extract_years(text: str) -> int:
    """Extracts numerical years of experience."""
    match = re.search(r"(\d+)\s*\+?\s*(years?|yrs?)", text.lower())
    return int(match.group(1)) if match else 0

def score_applicant(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """Calculates overall compatibility score."""
    resume_sections = split_resume_sections(resume_text)
    jd_sections = split_jd_sections(jd_text)

    experience_score = embed_text(resume_sections.get("experience", ""), jd_sections.get("experience", ""))
    skill_score = jaccard_similarity(extract_skills(resume_sections.get("skills", "")), extract_skills(jd_sections.get("skills", "")))
    education_score = match_education(resume_sections.get("education", ""), jd_sections.get("education", ""))

    resume_years = extract_years(resume_sections.get("experience", ""))
    jd_required_years = extract_years(jd_sections.get("experience", ""))
    years_score = 0.0
    if jd_required_years > 0:
        years_score = min(resume_years / jd_required_years, 1.0)
    elif resume_years > 0 and jd_required_years == 0:
        years_score = 0.75
    else:
        years_score = 1.0

    W_EXPERIENCE = 0.35
    W_SKILL = 0.35
    W_EDUCATION = 0.20
    W_YEARS = 0.10

    total_score = (experience_score * W_EXPERIENCE + skill_score * W_SKILL + education_score * W_EDUCATION + years_score * W_YEARS) * 100

    status = "Disqualified"
    if total_score >= 70: status = "Qualified"
    elif total_score >= 45: status = "Maybe"

    return {
        "score": round(total_score, 1),
        "status": status,
        "section_scores": {
            "experience_score": round(experience_score, 2),
            "skill_score": round(skill_score, 2),
            "education_score": round(education_score, 2),
            "years_score": round(years_score, 2)
        },
        "extracted_content": {
            "resume": {
                "experience": resume_sections.get("experience", ""), "skills": list(extract_skills(resume_sections.get("skills", ""))),
                "education": resume_sections.get("education", ""), "years_experience": resume_years,
                "education_norm": normalize_degrees(resume_sections.get("education", "")),
                "education_fields": list(extract_field_keywords(normalize_degrees(resume_sections.get("education", ""))))
            },
            "jd": {
                "experience": jd_sections.get("experience", ""), "skills": list(extract_skills(jd_sections.get("skills", ""))),
                "education": jd_sections.get("education", ""), "required_years": jd_required_years,
                "education_norm": normalize_degrees(jd_sections.get("education", "")),
                "education_fields": list(extract_field_keywords(normalize_degrees(jd_sections.get("education", ""))))
            }
        }
    }