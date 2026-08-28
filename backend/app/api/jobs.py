from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_recruiter
from app.db.dependencies import get_db
from app.models.recruiter import Recruiter
from app.dto.job_parameter import (
    JobParameterCreate,
    JobParameterResponse,
    JobParameterUpdate,
)
from app.services.job_service import (
    create_job,
    get_recruiter_jobs,
    get_job_by_id,
    update_job,
    delete_job
)

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


@router.get(
    "",
    response_model=list[JobParameterResponse]
)
def get_jobs(
    db: Session = Depends(get_db),
    current_recruiter: Recruiter = Depends(
        get_current_recruiter
    ),
):
    return get_recruiter_jobs(
        db=db,
        recruiter_id=current_recruiter.recruiter_id,
    )

@router.get(
    "/{job_id}",
    response_model=JobParameterResponse,
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_recruiter: Recruiter = Depends(
        get_current_recruiter
    ),
):
    job = get_job_by_id(
        db=db,
        job_id=job_id,
        recruiter_id=current_recruiter.recruiter_id,
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job

@router.put(
    "/{job_id}",
    response_model=JobParameterResponse,
)
def update_job_api(
    job_id: int,
    job_data: JobParameterUpdate,
    db: Session = Depends(get_db),
    current_recruiter: Recruiter = Depends(
        get_current_recruiter
    ),
):
    job = update_job(
        db=db,
        job_id=job_id,
        recruiter_id=current_recruiter.recruiter_id,
        job_data=job_data,
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job

@router.delete("/{job_id}")
def delete_job_api(
    job_id: int,
    db: Session = Depends(get_db),
    current_recruiter: Recruiter = Depends(
        get_current_recruiter
    ),
):
    deleted = delete_job(
        db=db,
        job_id=job_id,
        recruiter_id=current_recruiter.recruiter_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return {
        "message": "Job deleted successfully"
    }