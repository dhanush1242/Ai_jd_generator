from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.dto.candidate import CandidateCreate
from app.models.candidate import Candidate

def get_candidate_by_email(db: Session, email: str,):
    return (db.query(Candidate).filter(Candidate.email == email).first())

def get_candidate_by_mobile(db: Session, mobile_number: str,):
    return (db.query(Candidate).filter(Candidate.mobile_number == mobile_number).first())

def create_candidate(db: Session, candidate_data: CandidateCreate,) -> Candidate:
    candidate = Candidate(
        name=candidate_data.name,
        email=candidate_data.email,
        hashed_password=hash_password(candidate_data.password),
        mobile_number=candidate_data.mobile_number,
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

def get_candidate_by_id(db: Session, candidate_id: int,):
    return (db.query(Candidate).filter(Candidate.candidate_id == candidate_id).first())