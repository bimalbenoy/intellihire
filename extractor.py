import io
import os
import requests
from pdfminer.high_level import extract_text as extract_pdf
import docx
def extract(url: str) -> str:
    #Download file
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code!=200:
            raise ValueError(f"Download failed: {response.status_code} for url: {url}")
        file_bytes = response.content #for extraction
    except Exception as e:
        return f'Download failed: {e}'
    
    #file detection
    content_type = response.headers.get("Content-Type","").lower()
    if "pdf" in content_type:
        file_type = "pdf"
    elif "docx" in content_type or "word" in content_type:
        file_type = "docx"
    else:
        if url.endswith(".pdf"):
            file_type = "pdf"
        elif url.endswith(".docx"):
            file_type = "docx"
        else:
            return "Unknown file type — must be .pdf or .docx or a correct content-type."
    if file_type=="pdf":
        with io.BytesIO(file_bytes) as pdf_file:
            return extract_pdf(pdf_file)
    elif file_type=="docx":
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            return f"failed to extract DOC text: {e}"
    else:
        return "Unsupported file type"
if __name__ == "__main__":
    url = "https://cdn.eycareercenter.com/Resume-Samples.pdf"
    try:
        text = extract(url)
        print("✅ Extracted Text Preview:\n")
        print(text[:1000])  # preview the first 1000 characters
    except ValueError as e:
        print("❌ Error:", e)
