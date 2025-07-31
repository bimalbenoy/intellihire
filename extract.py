import os
import requests
from pdfminer.high_level import extract_text as extract_pdf
import docx

def extract(file_path: str) -> str:
    # If input is a URL, download the file temporarily
    if file_path.startswith("http"):
        print("🌐 Downloading file from URL...")
        r = requests.get(file_path)
        if r.status_code != 200:
            raise Exception(f"Failed to download file: {file_path}")
        
        # Infer file type from URL
        ext = ".pdf" if ".pdf" in file_path else ".docx"
        temp_path = f"temp_resume{ext}"
        with open(temp_path, "wb") as f:
            f.write(r.content)
        
        text = extract(temp_path)
        os.remove(temp_path)
        return text

    # Local PDF
    if file_path.endswith('.pdf'):
        return extract_pdf(file_path)
    # Local DOCX
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Unsupported file type. Use .pdf or .docx")
