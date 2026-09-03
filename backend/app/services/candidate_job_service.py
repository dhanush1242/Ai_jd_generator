from sqlalchemy.orm import Session
from app.models.job_parameter import JobParameter
from app.models.job_description import JobDescription

def get_published_jobs(db: Session, location: str | None = None, experience: str | None = None, skills: str | None = None,):
    query = (db.query(JobParameter, JobDescription).join(JobDescription,JobDescription.job_id == JobParameter.job_id,)
        .filter(JobDescription.is_published == True))
    if location: query = query.filter(JobParameter.location.ilike(f"%{location}%"))
    if experience: query = query.filter(JobParameter.experience.ilike(f"%{experience}%"))
    if skills: query = query.filter(JobParameter.required_skills.ilike(f"%{skills}%"))
    jobs = query.all()
    result = []
    for job, jd in jobs:
        result.append(
            {
                "job_id": job.job_id,
                "job_title": job.job_title,
                "required_skills": job.required_skills,
                "education_qualification": job.education_qualification,
                "experience": job.experience,
                "location": job.location,
                "passedout_year": job.passedout_year,
                "work_mode": job.work_mode,
                "job_type": job.job_type,
                "package": job.package,
                "jd_id": jd.jd_id,
                "version_number": jd.version_number,
                "job_description": jd.updated_jd or jd.generated_jd,
                "published_at": jd.published_at,
            }
        )
    return result