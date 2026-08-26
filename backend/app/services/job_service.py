from sqlalchemy.orm import Session

from app.models.job_parameter import JobParameter
from app.models.recruiter import Recruiter
from app.schemas.job_parameter import JobParameterCreate


def create_job(
    db: Session,
    job_data: JobParameterCreate,
    recruiter: Recruiter,
) -> JobParameter:

    job = JobParameter(
        recruiter_id=recruiter.recruiter_id,
        job_title=job_data.job_title,
        required_skills=job_data.required_skills,
        education_qualification=(
            job_data.education_qualification
        ),
        experience=job_data.experience,
        location=job_data.location,
        passedout_year=job_data.passedout_year,
        work_mode=job_data.work_mode,
        job_type=job_data.job_type,
        package=job_data.package,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job