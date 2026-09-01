from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dto.candidate_details import CandidateDetailsCreate
from app.models.candidate import Candidate
from app.models.candidate_details import CandidateDetails

def create_candidate_details(db: Session, details_data: CandidateDetailsCreate, candidate: Candidate,) -> CandidateDetails:
    existing_details = (db.query(CandidateDetails).filter(CandidateDetails.candidate_id== candidate.candidate_id).first())
    if existing_details:raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Candidate details already exist",)
    details = CandidateDetails(candidate_id=candidate.candidate_id, **details_data.model_dump(),)
    db.add(details)
    db.commit()
    db.refresh(details)
    return details

def get_candidate_details(db: Session, candidate: Candidate,) -> CandidateDetails:
    details = (db.query(CandidateDetails).filter(CandidateDetails.candidate_id== candidate.candidate_id).first())
    if not details:raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Candidate details not found",)
    return details