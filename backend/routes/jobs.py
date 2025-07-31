from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel
from beanie import PydanticObjectId

from models import Job, JobStatus, Application, User, Role, ApplicationStatus
from security import get_current_user

router = APIRouter()

class JobApplicationRequest(BaseModel):
    resume: str
    cover_letter: str = None

@router.get(
    "/",
    response_model=List[Job],
    summary="Get all open job listings"
)
async def get_all_open_jobs():
    jobs = await Job.find(Job.status == JobStatus.OPEN).to_list()
    return jobs


@router.post("/{job_id}/apply", status_code=status.HTTP_201_CREATED)
async def apply_for_job(
    job_id: PydanticObjectId,
    application_data: JobApplicationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Apply for a job.
    Only CANDIDATE users can apply for jobs.
    """
    # Check if user is a candidate
    if current_user.role != Role.CANDIDATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can apply for jobs."
        )
    
    # Check if job exists and is open
    job = await Job.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found."
        )
    
    if job.status != JobStatus.OPEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This job is no longer accepting applications."
        )
    
    # Check if user has already applied for this job
    existing_application = await Application.find_one(
        Application.job_id == job_id, 
        Application.candidate_id == current_user.id
    )
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job."
        )
    
    # Create new application
    new_application = Application(
        job_id=job_id,
        candidate_id=current_user.id,
        resume=application_data.resume,
        cover_letter=application_data.cover_letter,
        status=ApplicationStatus.APPLIED
    )
    
    await new_application.insert()
    
    return {
        "message": f"Successfully applied for {job.title} at {job.company}",
        "application_id": str(new_application.id),
        "job_title": job.title,
        "company": job.company,
        "applied_at": new_application.applied_at,
        "status": new_application.status
    }