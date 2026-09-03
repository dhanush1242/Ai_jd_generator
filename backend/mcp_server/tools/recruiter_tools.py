from mcp_server.database import get_db_session
from app.models.job_parameter import JobParameter
from app.models.job_description import JobDescription
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.candidate_details import CandidateDetails
from app.models.application_note import ApplicationNote

def get_recruiter_jobs(recruiter_id: int,) -> list[dict]:
    """
    Get all jobs created by a recruiter.

    Returns one row per job using the latest
    JD version for that job.
    """
    db = get_db_session()
    try:
        jobs = (
            db.query(JobParameter)
            .filter(JobParameter.recruiter_id == recruiter_id)
            .order_by(JobParameter.job_id.desc()).all())
        result = []
        for job in jobs:
            latest_jd = (
                db.query(JobDescription)
                .filter(JobDescription.job_id == job.job_id)
                .order_by(JobDescription.version_number.desc()).first())
            result.append(
                {
                    "job_id": job.job_id,
                    "job_title": job.job_title,
                    "required_skills": job.required_skills,
                    "experience": job.experience,
                    "location": job.location,
                    "work_mode": job.work_mode,
                    "job_type": job.job_type,
                    "package": job.package,
                    "jd_id": (latest_jd.jd_id
                        if latest_jd else None),
                    "version_number": (latest_jd.version_number
                        if latest_jd else None),
                    "is_published": (latest_jd.is_published
                        if latest_jd else False),
                }
            )

        return result
    finally: db.close()

def get_job_applications(recruiter_id: int, job_id: int,) -> list[dict]:
    """
    Get applications for a recruiter-owned job.
    """
    db = get_db_session()
    try:
        job = (db.query(JobParameter).filter(JobParameter.job_id == job_id).first())
        if job is None:
            return {"found": False, "message": "Job not found"} # pyright: ignore[reportReturnType]
        if job.recruiter_id != recruiter_id:
            return {
                "found": False,
                "message": (
                    "You are not authorized to view "
                    "applications for this job"
                ),
            } # pyright: ignore[reportReturnType]
        records = (
            db.query(Application, Candidate, CandidateDetails,)
            .join(Candidate, Candidate.candidate_id == Application.candidate_id,)
            .outerjoin(CandidateDetails, CandidateDetails.candidate_id == Candidate.candidate_id,)
            .filter(Application.job_id == job_id)
            .order_by(Application.created_at.desc()).all())
        applications = []
        for application, candidate, details in records:
            applications.append(
                {
                    "application_id": (application.application_id),
                    "candidate_id": (candidate.candidate_id),
                    "candidate_name": candidate.name,
                    "candidate_email": candidate.email,
                    "mobile_number": (candidate.mobile_number),
                    "education_qualification": (details.education_qualification
                        if details else None),
                    "experience": (details.experience
                        if details else None),
                    "skills": (details.skills
                        if details else None),
                    "status": application.status,
                    "applied_at": (application.created_at.isoformat()),
                }
            )
        return applications

    finally: db.close()

def get_application_notes(recruiter_id: int, application_id: int,) -> list[dict] | dict:
    """
    Get recruiter notes for an application.
    """
    db = get_db_session()
    try:
        application = (db.query(Application).filter(Application.application_id == application_id).first())
        if application is None:
            return {"found": False, "message": "Application not found",}

        job = (db.query(JobParameter).filter(JobParameter.job_id == application.job_id).first())
        if job is None:
            return {"found": False, "message": "Job not found",}
        if job.recruiter_id != recruiter_id:
            return {
                "found": False,
                "message": (
                    "You are not authorized to view "
                    "notes for this application"
                ),
            }

        notes = (
            db.query(ApplicationNote)
            .filter(ApplicationNote.application_id == application_id)
            .order_by(ApplicationNote.created_at.desc()).all())
        return [
            {
                "note_id": note.note_id,
                "application_id": note.application_id,
                "recruiter_id": note.recruiter_id,
                "notes": note.notes,
                "created_at": note.created_at.isoformat(),
            }
            for note in notes
        ]

    finally: db.close()