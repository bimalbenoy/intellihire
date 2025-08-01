# backend/routes/utils.py
from fastapi import APIRouter, UploadFile, File
from extractor_local import extract_resume_data
from rejection_mails import send_rejection_email

router = APIRouter()

@router.post("/extract-resume")
async def extract_resume(file: UploadFile = File(...)):
    content = await file.read()
    # Pass content to your extractor function (modify it if needed)
    result = extract_resume_data(content)
    return {"extracted_data": result}

@router.post("/send-rejection")
def send_rejection(email: str, reason: str):
    result = send_rejection_email(email, reason)
    return {"status": result}

