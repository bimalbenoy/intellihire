import cloudinary.uploader
from cloudinary_config import cloudinary  # This will load your .env automatically
import sys
import os

def upload_resume(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.endswith((".pdf", ".docx")):
        raise ValueError("Only .pdf and .docx files are supported.")

    print(f"📤 Uploading {file_path} to Cloudinary...")

    response = cloudinary.uploader.upload(
        file_path,
        resource_type="raw",  # Use raw for non-image files like PDF/DOCX
        folder="resumes"      # Optional: organize into a folder in your Cloudinary account
    )

    url = response.get("secure_url")
    if not url:
        raise Exception("Failed to get URL from Cloudinary response.")

    print("✅ Upload successful.")
    return url

if __name__ == "__main__":
    # Optional: allow filename as CLI arg
    file_path = sys.argv[1] if len(sys.argv) > 1 else "test_resume.pdf"
    try:
        url = upload_resume(file_path)
        print("🔗 Cloudinary File URL:", url)
    except Exception as e:
        print("❌ Error:", e)
