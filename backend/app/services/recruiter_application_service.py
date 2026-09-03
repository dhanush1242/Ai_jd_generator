import os
from fastapi.responses import FileResponse
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.application import Application
from app.models.job_parameter import JobParameter
from app.models.candidate import Candidate
from app.models.candidate_details import CandidateDetails

def get_job_applications(db: Session, recruiter_id: int, job_id: int,):
    job = (db.query(JobParameter).filter(JobParameter.job_id == job_id).first())
    if job is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found",)
    if job.recruiter_id != recruiter_id: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view applications for this job",)

    records = (
        db.query(Application, Candidate, CandidateDetails,)
        .join(Candidate, Candidate.candidate_id == Application.candidate_id,)
        .outerjoin(CandidateDetails, CandidateDetails.candidate_id == Candidate.candidate_id,)
        .filter(Application.job_id == job_id)
        .order_by(Application.created_at.desc()).all())
    result = []

    for application, candidate, details in records:
        result.append(
            {
                "application_id": application.application_id,
                "candidate_id": candidate.candidate_id,
                "candidate_name": candidate.name,
                "candidate_email": candidate.email,
                "mobile_number": candidate.mobile_number,
                "education_qualification": (details.education_qualification
                    if details else None),
                "passedout_year": (details.passedout_year
                    if details else None),
                "experience": (details.experience
                    if details else None),
                "skills": (details.skills
                    if details else None),
                "resume_url": application.resume_url,
                "github_url": (details.github_url
                    if details else None),
                "linkedin_url": (details.linkedin_url
                    if details else None),
                "job_id": application.job_id,
                "jd_id": application.jd_id,
                "status": application.status,
                "created_at": application.created_at,
                "updated_at": application.updated_at,
            }
        )
    return result

def update_application_status(db: Session, recruiter_id: int, application_id: int, new_status: str,):
    allowed_statuses = {"applied", "shortlisted", "rejected",}
    if new_status not in allowed_statuses: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid application status",)

    application = (db.query(Application).filter(Application.application_id == application_id).first())
    if application is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found",)

    job = (db.query(JobParameter).filter(JobParameter.job_id == application.job_id).first())
    if job is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found",)
    if job.recruiter_id != recruiter_id: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this application",)

    application.status = new_status

    db.commit()
    db.refresh(application)
    return application

def get_application_resume(db: Session, recruiter_id: int, application_id: int,):
    application = (db.query(Application).filter(Application.application_id == application_id).first())
    if application is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found",)

    job = (db.query(JobParameter).filter(JobParameter.job_id == application.job_id).first())
    if job is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found",)
    if job.recruiter_id != recruiter_id: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this resume",)

    resume_path = application.resume_url
    if not resume_path or not os.path.exists(resume_path): raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume file not found",)
    return FileResponse(path=resume_path, media_type="application/pdf", filename=os.path.basename(resume_path),)