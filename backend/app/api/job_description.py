from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_current_recruiter
from app.db.dependencies import get_db
from app.models.recruiter import Recruiter
from app.dto.job_description import (
    JobDescriptionResponse,
    JobDescriptionUpdate,
)
from app.services.job_description_service import (
    generate_jd,
    regenerate_jd,
    get_jd_versions,
    update_jd_version,
    publish_jd_version,
)


router = APIRouter(
    prefix="/jobs",
    tags=["JD"],
)


@router.post(
    "/{job_id}/generate-jd",
    response_model=JobDescriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_generated_jd(
    job_id: int,
    db: Session = Depends(get_db),
    current_recruiter: Recruiter = Depends(get_current_recruiter),
):
    return generate_jd(
        db=db,
        job_id=job_id,
        recruiter=current_recruiter,
    )


@router.post(
    "/{job_id}/regenerate-jd",
    response_model=JobDescriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_regenerated_jd(
    job_id: int,
    db: Session = Depends(get_db),
    current_recruiter: Recruiter = Depends(get_current_recruiter),
):
    return regenerate_jd(
        db=db,
        job_id=job_id,
        recruiter=current_recruiter,
    )


@router.put(
    "/{job_id}/versions/{version_id}",
    response_model=JobDescriptionResponse,
)
def update_jd_by_version(
    job_id: int,
    version_id: int,
    update_data: JobDescriptionUpdate,
    db: Session = Depends(get_db),
    current_recruiter: Recruiter = Depends(get_current_recruiter),
):
    return update_jd_version(
        db=db,
        job_id=job_id,
        version_id=version_id,
        update_data=update_data,
        recruiter=current_recruiter,
    )


@router.get(
    "/{job_id}/versions",
    response_model=List[JobDescriptionResponse],
)
def read_jd_versions(
    job_id: int,
    db: Session = Depends(get_db),
    current_recruiter: Recruiter = Depends(get_current_recruiter),
):
    return get_jd_versions(
        db=db,
        job_id=job_id,
        recruiter=current_recruiter,
    )


@router.post(
    "/{job_id}/versions/{version_id}/publish",
    response_model=JobDescriptionResponse,
)
def publish_jd_by_version(
    job_id: int,
    version_id: int,
    db: Session = Depends(get_db),
    current_recruiter: Recruiter = Depends(get_current_recruiter),
):
    return publish_jd_version(
        db=db,
        job_id=job_id,
        version_id=version_id,
        recruiter=current_recruiter,
    )
