from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from beanie import PydanticObjectId

from models import User, Job, Application, Role, ApplicationForRecruiter, CandidateInfo
from security import get_current_user

router = APIRouter()

@router.get("/jobs/{id}/applications", response_model=List[ApplicationForRecruiter])
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
    if current_user.role == Role.ADMIN and job.posted_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view applications for jobs that you have posted."
        )
    applications = await Application.find(Application.job_id == job_id).to_list()

    if not applications:
        return []
    
    response_data: List[ApplicationForRecruiter] = []
    for app in applications:
        candidate = await User.get(app.candidate_id)
        if candidate:
            candidate_info = CandidateInfo(
                id=candidate.id,
                full_name=candidate.full_name,
                email=candidate.email,
            )
            app_for_recruiter = ApplicationForRecruiter(
                id=app.id,
                job_id=app.job_id,
                resume_url=app.resume_url,
                ai_match_score=app.ai_match_score,
                status=app.status,
                applied_at=app.applied_at,
                candidate=candidate_info
            )
            response_data.append(app_for_recruiter)
    response_data.sort(key=lambda x: x.ai_match_score, reverse=True)
    return response_data


@router.get("/my-jobs", response_model=List[Job])
async def get_my_posted_jobs(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view posted jobs."
        )
    jobs = await Job.find(Job.posted_by_id == current_user.id).to_list()

    return jobs