from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_recruiter
from app.db.dependencies import get_db
from app.models.recruiter import Recruiter
from app.schemas.job_parameter import (
    JobParameterCreate,
    JobParameterResponse,
)
from app.services.job_service import create_job


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=JobParameterResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_job(
    job_data: JobParameterCreate,
    db: Session = Depends(get_db),
    current_recruiter: Recruiter = Depends(
        get_current_recruiter
    ),
):
    return create_job(
        db=db,
        job_data=job_data,
        recruiter=current_recruiter,
    )