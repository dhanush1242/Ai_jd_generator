from mcp_server.database import get_db_session
from app.models.job_parameter import JobParameter
from app.models.job_description import JobDescription
from app.models.application import Application

def search_jobs(location: str | None = None, experience: str | None = None, skills: str | None = None,) -> list[dict]:
    """
    Search published jobs using optional filters.
    """
    db = get_db_session()
    try:
        query = (
            db.query(JobParameter, JobDescription,)
            .join(JobDescription, JobDescription.job_id == JobParameter.job_id,)
            .filter(JobDescription.is_published == True))
        if location: query = query.filter(JobParameter.location.ilike(f"%{location}%"))
        if experience: query = query.filter(JobParameter.experience.ilike(f"%{experience}%"))
        if skills: query = query.filter(JobParameter.required_skills.ilike(f"%{skills}%"))

        records = query.all()
        jobs = []
        for job, jd in records:
            jobs.append(
                {
                    "job_id": job.job_id,
                    "job_title": job.job_title,
                    "required_skills": job.required_skills,
                    "education_qualification": (job.education_qualification),
                    "experience": job.experience,
                    "location": job.location,
                    "work_mode": job.work_mode,
                    "job_type": job.job_type,
                    "package": job.package,
                    "jd_id": jd.jd_id,
                    "version_number": jd.version_number,
                    "job_description": (jd.updated_jd or jd.generated_jd),
                }
            )

        return jobs
    finally: db.close()

def get_my_applications(candidate_id: int,) -> list[dict]:
    """
    Get all job applications for a candidate.
    """
    db = get_db_session()
    try:
        records = (
            db.query(Application, JobParameter,)
            .join(JobParameter, JobParameter.job_id == Application.job_id,)
            .filter(Application.candidate_id == candidate_id)
            .order_by(Application.created_at.desc()).all())
        applications = []
        for application, job in records:
            applications.append(
                {
                    "application_id": application.application_id,
                    "job_id": application.job_id,
                    "job_title": job.job_title,
                    "location": job.location,
                    "experience": job.experience,
                    "work_mode": job.work_mode,
                    "job_type": job.job_type,
                    "package": job.package,
                    "status": application.status,
                    "applied_at": (application.created_at.isoformat()),
                }
            )
        return applications
    finally: db.close()

def get_application_status(candidate_id: int, job_title: str,) -> dict:
    """
    Get the application status for a candidate
    using the job title.
    """
    db = get_db_session()
    try:
        record = (
            db.query(Application, JobParameter,)
            .join(JobParameter, JobParameter.job_id == Application.job_id,)
            .filter(Application.candidate_id == candidate_id, JobParameter.job_title.ilike(f"%{job_title}%"),).first())

        if record is None:
            return {"found": False, "message": (f"No application found for {job_title}"),}
        application, job = record
        return {
            "found": True,
            "application_id": application.application_id,
            "job_id": job.job_id,
            "job_title": job.job_title,
            "status": application.status,
            "applied_at": application.created_at.isoformat(),
        }
    finally: db.close()