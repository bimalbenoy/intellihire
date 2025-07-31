import requests
import json
from extract import extract

# === 1. Cloudinary Resume URL ===
resume_path = "https://res.cloudinary.com/dt4teetku/raw/upload/v1753972749/resumes/zexkf4e3jfa2usfywvir.pdf"

# === 2. Extract Resume Text ===
resume_text = extract(resume_path)

# === 3. Dummy Job Description ===
job_description = """Education:
Bachelor's degree in Computer Science or related field

Skills:
Python, Django, AWS, Docker, CI/CD, REST APIs

Experience:
3+ years experience in backend development
Must have experience deploying apps to AWS and building RESTful APIs
"""

# === 4. Prepare Payload ===
payload = {
    "resume": resume_text,
    "job_description": job_description
}

# 🔽 Save payload to file for inspection/debugging
with open("payload.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

# === 5. Send to /score API ===
url = "http://127.0.0.1:8000/score"
response = requests.post(url, json=payload)

# === 6. Output Result ===
if response.status_code == 200:
    data = response.json()
    print("\n🎯 Match Score:", data["score"])
    print("📊 Section Scores:", data["section_scores"])
    print("✅ Status:", data["status"])
else:
    print("❌ API call failed:", response.text)
