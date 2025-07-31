from fastapi import FastAPI, Depends,HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from fastapi.middleware.cors import CORSMiddleware

from models import User, Job, Application
from routes import auth, jobs, recruiterView
from security import get_current_user

app=FastAPI(title="IntelliHire AI ATS")

origins = [
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def app_init():

    client=AsyncIOMotorClient("mongodb+srv://codemasters:codeMastersPass@intellihire.mroevwy.mongodb.net/?retryWrites=true&w=majority&appName=intellihire")
    

    await init_beanie(database=client.intellihire, document_models=[User, Job, Application])

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(application.router, prefix="/applications", tags=["Applications"])
app.include_router(recruiterView.router, prefix="/recruiter", tags=["Recruiter Tools"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"]) 

@app.get("/users/me",response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/")

def read_root():
    return {"message": "Welcome to IntelliHire AI ATS!"}