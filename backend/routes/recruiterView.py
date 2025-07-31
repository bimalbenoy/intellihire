from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from beanie import PydanticObjectId

from pydantic import BaseModel, EmailStr

from models import User, Job, Application, Role, ApplicationforRecruiter, CandidateInfo, JobCreate, ApplicationStatus
from security import get_current_user

router = APIRouter()

class AssignReviewerRequest(BaseModel):
    reviewer_email: EmailStr

class UpdateApplicationStatusRequest(BaseModel):
    status: ApplicationStatus

@router.post("/jobs/{job_id}/assign-reviewer")
async def assign_reviewer_to_job(
    job_id: PydanticObjectId,
    request: AssignReviewerRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Assign a reviewer to a job by their email.
    Only ADMIN users who posted the job can assign reviewers.
    """
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to assign reviewers."
        )
    
    # Find the job
    job = await Job.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found."
        )
    
    # Check if current user posted this job
    if job.posted_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only assign reviewers to jobs you have posted."
        )
    
    # Find the reviewer by email
    reviewer = await User.find_one(User.email == request.reviewer_email)
    if not reviewer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found with email: {request.reviewer_email}"
        )
    
    # Check if the user has REVIEWER role
    if reviewer.role != Role.REVIEWER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The specified user is not a reviewer. Only users with REVIEWER role can be assigned."
        )
    
    # Assign the reviewer to the job
    job.reviewer_id = reviewer.id
    await job.save()
    
    return {
        "message": f"Reviewer {reviewer.full_name} ({reviewer.email}) has been assigned to job '{job.title}'",
        "job_id": str(job.id),
        "reviewer_id": str(reviewer.id),
        "reviewer_name": reviewer.full_name,
        "reviewer_email": reviewer.email
    }

@router.get("/jobs/{id}/applications", response_model=List[ApplicationforRecruiter])
async def get_applications_for_job(
    job_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [Role.ADMIN, Role.REVIEWER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view applications."
        )
    
    job = await Job.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found."
        )
    if (current_user.role == Role.ADMIN and job.posted_by_id != current_user.id) or (current_user.role == Role.REVIEWER and job.reviewer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view applications for jobs that you have posted."
        )
    applications = await Application.find(Application.job_id == job_id).to_list()

    if not applications:
        return []
    
    response_data: List[ApplicationforRecruiter] = []
    for app in applications:
        candidate = await User.get(app.candidate_id)
        if candidate:
            candidate_info = CandidateInfo(
                id=candidate.id,
                full_name=candidate.full_name,
                email=candidate.email,
            )
            app_for_recruiter = ApplicationforRecruiter(
                id=app.id,
                job_id=app.job_id,
                resume=app.resume,
                ai_match_score=app.ai_match_score,
                status=app.status,
                applied_at=app.applied_at,
                candidate=candidate_info
            )
            response_data.append(app_for_recruiter)
    response_data.sort(key=lambda x: x.ai_match_score, reverse=True)
    return response_data


@router.put("/applications/{application_id}/status")
async def update_application_status(
    application_id: PydanticObjectId,
    request: UpdateApplicationStatusRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Accept or reject an application.
    Only ADMIN (job poster) or REVIEWER (assigned to job) can update application status.
    """
    if current_user.role not in [Role.ADMIN, Role.REVIEWER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update application status."
        )
    
    # Find the application
    application = await Application.get(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found."
        )
    
    # Find the related job
    job = await Job.get(application.job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Related job not found."
        )
    
    # Authorization check
    if current_user.role == Role.ADMIN:
        # Admin can only update applications for jobs they posted
        if job.posted_by_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update applications for jobs you have posted."
            )
    elif current_user.role == Role.REVIEWER:
        # Reviewer can only update applications for jobs they are assigned to
        if job.reviewer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update applications for jobs you are assigned to review."
            )
    
    # Validate status transition
    if request.status == ApplicationStatus.APPLIED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change status back to 'applied'. Only 'shortlisted' or 'rejected' are allowed."
        )
    
    # Update the application status
    old_status = application.status
    application.status = request.status
    await application.save()
    
    # Get candidate info for response
    candidate = await User.get(application.candidate_id)
    
    return {
        "message": f"Application status updated from '{old_status}' to '{request.status}'",
        "application_id": str(application.id),
        "job_title": job.title,
        "candidate_name": candidate.full_name if candidate else "Unknown",
        "candidate_email": candidate.email if candidate else "Unknown",
        "old_status": old_status,
        "new_status": request.status,
        "updated_by": current_user.full_name
    }


@router.post("/jobs", response_model=Job, status_code=status.HTTP_201_CREATED)
async def create_job_listing(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to post jobs."
        )
    
    new_job = Job(
        title=job_data.title,
        company=job_data.company,
        description=job_data.description,
        location=job_data.location,
        posted_by_id=current_user.id
    )
    await new_job.insert()
    
    return new_job


@router.get("/my-jobs", response_model=List[Job])
async def get_my_posted_jobs(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view posted jobs."
        )
    jobs = await Job.find(Job.posted_by_id == current_user.id).to_list()

    return jobs