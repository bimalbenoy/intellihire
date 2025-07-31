from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Role(str,Enum):
    CANDIDATE = "candidate"
    ADMIN = "admin"
    REVIEWER = "reviewer"

class JobStatus(str,Enum):
    OPEN = "open"
    CLOSED = "closed"

class CandidateInfo(BaseModel):
    id: PydanticObjectId
    full_name: str
    email: EmailStr

class ApplicationStatus(str,Enum):
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"

class ApplicationforRecruiter(BaseModel):
    id: PydanticObjectId
    job_id: PydanticObjectId
    candidate: CandidateInfo
    resume: str 
    cover_letter: Optional[str] = None
    ai_match_score: float = 0.0
    status: ApplicationStatus
    applied_at: datetime

class User(Document):
    full_name: str
    email: EmailStr
    hashed_password: str
    role: Role = Role.CANDIDATE
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

class Job(Document):
    title: str
    company: str
    description: str
    location: str
    status: JobStatus = JobStatus.OPEN
    posted_by_id: PydanticObjectId
    reviewer_id: Optional[PydanticObjectId] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "jobs"

class Application(Document):
    job_id: PydanticObjectId
    candidate_id: PydanticObjectId
    resume: str 
    cover_letter: Optional[str] = None
    ai_match_score: float = 0.0
    status: ApplicationStatus = ApplicationStatus.APPLIED
    applied_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "applications"

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    location: str
    reviewer_id: Optional[PydanticObjectId] = None