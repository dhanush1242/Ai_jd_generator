from sqlalchemy.orm import Session
from app.dto.job_parameter import JobParameterCreate, JobParameterUpdate
from app.models.job_parameter import JobParameter
from app.models.recruiter import Recruiter

def create_job(db: Session, job_data: JobParameterCreate, recruiter: Recruiter,) -> JobParameter:
    job = JobParameter(
        recruiter_id=recruiter.recruiter_id,
        job_title=job_data.job_title,
        required_skills=job_data.required_skills,
        education_qualification=(job_data.education_qualification),
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

def get_recruiter_jobs(db: Session, recruiter_id: int,):
    jobs = (db.query(JobParameter).filter(JobParameter.recruiter_id == recruiter_id).all())
    return jobs

def get_job_by_id(db: Session, job_id: int, recruiter_id: int,):
    job = (db.query(JobParameter).filter(JobParameter.job_id == job_id, JobParameter.recruiter_id == recruiter_id,).first())
    return job

def update_job(db: Session, job_id: int, recruiter_id: int, job_data: JobParameterUpdate,):
    job = (db.query(JobParameter).filter(JobParameter.job_id == job_id, JobParameter.recruiter_id == recruiter_id,).first())
    if not job: return None
    update_data = job_data.model_dump(exclude_unset=True)
    for field, value in update_data.items(): setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job

def delete_job(db: Session, job_id: int, recruiter_id: int,):
    job = (db.query(JobParameter).filter(JobParameter.job_id == job_id, JobParameter.recruiter_id == recruiter_id,).first())
    if not job: return False
    db.delete(job)
    db.commit()
    return True