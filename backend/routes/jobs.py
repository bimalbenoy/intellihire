from fastapi import APIRouter
from typing import List
from models import Job, JobStatus

router = APIRouter()

@router.get(
    "/",
    response_model=List[Job],
    summary="Get all open job listings"
)
async def get_all_open_jobs():
    jobs = await Job.find(Job.status == JobStatus.OPEN).to_list()
    return jobs