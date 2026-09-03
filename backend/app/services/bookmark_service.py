from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.bookmark import Bookmark
from app.models.job_parameter import JobParameter
from app.models.job_description import JobDescription

def add_bookmark(db: Session, candidate_id: int, job_id: int,):
    job = (db.query(JobParameter).filter(JobParameter.job_id == job_id).first())
    if job is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found",)

    published_jd = (db.query(JobDescription).filter(JobDescription.job_id == job_id,JobDescription.is_published == True,).first())
    if published_jd is None: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job is not published",)

    existing_bookmark = (db.query(Bookmark).filter(Bookmark.candidate_id == candidate_id, Bookmark.job_id == job_id,).first())
    if existing_bookmark: raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Job already bookmarked",)

    bookmark = Bookmark(candidate_id=candidate_id, job_id=job_id,)

    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark

def get_candidate_bookmarks(db: Session, candidate_id: int,):
    return (db.query(Bookmark).filter(Bookmark.candidate_id == candidate_id).order_by(Bookmark.created_at.desc()).all())

def remove_bookmark(db: Session, candidate_id: int, job_id: int,):
    bookmark = (db.query(Bookmark).filter(Bookmark.candidate_id == candidate_id, Bookmark.job_id == job_id,).first())
    if bookmark is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found",)

    db.delete(bookmark)
    db.commit()
    return {"message": "Bookmark removed successfully"}