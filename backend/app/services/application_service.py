from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.candidate_details import CandidateDetails
from app.models.job_parameter import JobParameter
from app.models.job_description import JobDescription


def apply_for_job(
    db: Session,
    candidate_id: int,
    job_id: int,
):
    # 1. Check whether job exists
    job = (
        db.query(JobParameter)
        .filter(JobParameter.job_id == job_id)
        .first()
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # 2. Get the currently published JD
    published_jd = (
        db.query(JobDescription)
        .filter(
            JobDescription.job_id == job_id,
            JobDescription.is_published == True,
        )
        .first()
    )

    if published_jd is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job is not published",
        )

    # 3. Get candidate details
    candidate_details = (
        db.query(CandidateDetails)
        .filter(
            CandidateDetails.candidate_id == candidate_id
        )
        .first()
    )

    if candidate_details is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complete candidate details before applying",
        )

    # 4. Candidate must have a resume
    if not candidate_details.resume:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Upload resume before applying",
        )

    # 5. Prevent duplicate application
    existing_application = (
        db.query(Application)
        .filter(
            Application.candidate_id == candidate_id,
            Application.job_id == job_id,
        )
        .first()
    )

    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already applied for this job",
        )

    # 6. Create application
    application = Application(
        candidate_id=candidate_id,
        job_id=job_id,
        jd_id=published_jd.jd_id,
        resume_url=candidate_details.resume,
        status="applied",
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def get_candidate_applications(
    db: Session,
    candidate_id: int,
):
    records = (
        db.query(
            Application,
            JobParameter,
        )
        .join(
            JobParameter,
            JobParameter.job_id == Application.job_id,
        )
        .filter(
            Application.candidate_id == candidate_id
        )
        .order_by(
            Application.created_at.desc()
        )
        .all()
    )

    result = []

    for application, job in records:
        result.append(
            {
                "application_id": application.application_id,
                "job_id": application.job_id,
                "jd_id": application.jd_id,

                "job_title": job.job_title,
                "location": job.location,
                "experience": job.experience,
                "work_mode": job.work_mode,
                "job_type": job.job_type,
                "package": job.package,

                "status": application.status,

                "created_at": application.created_at,
                "updated_at": application.updated_at,
            }
        )

    return result