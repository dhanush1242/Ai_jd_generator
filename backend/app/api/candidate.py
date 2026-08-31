from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.services.candidate_service import (create_candidate, get_candidate_by_email, get_candidate_by_mobile,)
from app.core.security import (create_access_token, verify_password)
from app.dto.candidate import (CandidateCreate, CandidateResponse, CandidateLogin,)
from app.dto.auth import TokenResponse
from app.api.dependencies import get_current_candidate
from app.models.candidate import Candidate
from app.api.dependencies import get_current_candidate
from app.dto.candidate_details import (CandidateDetailsCreate, CandidateDetailsResponse,)
from app.models.candidate import Candidate
from app.services.candidate_details_service import (create_candidate_details, get_candidate_details,)

router = APIRouter(prefix="/candidates", tags=["Candidates"],)

@router.post("/register", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED,)
def register_candidate(candidate_data: CandidateCreate, db: Session = Depends(get_db),):
    existing_email = get_candidate_by_email(db, candidate_data.email,)
    if existing_email: raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered",)
    existing_mobile = get_candidate_by_mobile(db, candidate_data.mobile_number,)
    if existing_mobile: raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mobile number already registered",)
    candidate = create_candidate(db, candidate_data,)
    return candidate

@router.post("/login", response_model=TokenResponse,)
def login_candidate(login_data: CandidateLogin, db: Session = Depends(get_db),):
    candidate = get_candidate_by_email(db, login_data.email,)
    if candidate is None:raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password",)
    password_is_valid = verify_password(login_data.password, candidate.hashed_password,)
    if not password_is_valid: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password",)
    access_token = create_access_token(subject=str(candidate.candidate_id))
    return TokenResponse(access_token=access_token, token_type="bearer",)

@router.get("/me", response_model=CandidateResponse,)
def get_my_profile(current_candidate: Candidate = Depends(get_current_candidate),):return current_candidate

@router.post("/details", response_model=CandidateDetailsResponse, status_code=status.HTTP_201_CREATED,)
def create_my_details(details_data: CandidateDetailsCreate, current_candidate: Candidate = Depends(get_current_candidate), db: Session = Depends(get_db),):
    return create_candidate_details(db=db, details_data=details_data, candidate=current_candidate,)

@router.get("/details", response_model=CandidateDetailsResponse,)
def get_my_details(current_candidate: Candidate = Depends(get_current_candidate), db: Session = Depends(get_db),):
    return get_candidate_details(db=db, candidate=current_candidate,)