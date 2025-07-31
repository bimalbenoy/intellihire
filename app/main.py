from fastapi import FastAPI
from app.interface.routes.scoring import router as scoring_router

app = FastAPI(
    title="ATS Resume Scoring API",
    description="AI-powered resume and job description match scorer",
    version="1.0.0"
)

# Register the /score endpoint
app.include_router(scoring_router, prefix="", tags=["Scoring"])

@app.get("/")
def health_check():
    return {"message": "ATS AI Scoring Service is running 🚀"}

# ✅ Required for Windows (SBERT uses multiprocessing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
