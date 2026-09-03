from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.application import Application
from app.models.application_note import ApplicationNote
from app.models.job_parameter import JobParameter

def add_application_note(db: Session, recruiter_id: int, application_id: int, notes: str,):
    application = (db.query(Application).filter(Application.application_id == application_id).first())
    if application is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found",)

    job = (db.query(JobParameter).filter(JobParameter.job_id == application.job_id).first())
    if job is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found",)
    if job.recruiter_id != recruiter_id: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to add notes to this application",)
    if not notes.strip(): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Notes cannot be empty",)

    application_note = ApplicationNote(application_id=application_id, recruiter_id=recruiter_id, notes=notes.strip(), )
    db.add(application_note)
    db.commit()
    db.refresh(application_note)
    return application_note

def get_application_notes(db: Session, recruiter_id: int, application_id: int,):
    application = (db.query(Application).filter(Application.application_id == application_id).first())
    if application is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found",)

    job = (db.query(JobParameter).filter(JobParameter.job_id == application.job_id).first())
    if job is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found",)
    if job.recruiter_id != recruiter_id: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view notes for this application",)
    return (db.query(ApplicationNote).filter(ApplicationNote.application_id == application_id).order_by(ApplicationNote.created_at.desc()).all())