from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.dto.recruiter import (RecruiterCreate, RecruiterResponse,)
from app.services.recruiter_service import (create_recruiter, get_recruiter_by_email, get_recruiter_by_mobile,)
from app.core.security import (create_access_token, verify_password,)
from app.dto.auth import (RecruiterLogin, TokenResponse,)
from app.api.dependencies import get_current_recruiter
from app.models.recruiter import Recruiter
from app.dto.application import (
    RecruiterApplicationResponse,
    ApplicationStatusUpdate,
    ApplicationResponse,
)

from app.services.recruiter_application_service import (
    get_job_applications,
    update_application_status,
    get_application_resume,
)
from app.dto.application_note import (
    ApplicationNoteCreate,
    ApplicationNoteResponse,
)

from app.services.application_note_service import (
    add_application_note,
    get_application_notes,
)

router = APIRouter(prefix="/recruiters", tags=["Recruiters"],)

@router.post("/register", response_model=RecruiterResponse, status_code=status.HTTP_201_CREATED,)
def register_recruiter(recruiter_data: RecruiterCreate, db: Session = Depends(get_db),):
    existing_email = get_recruiter_by_email(db, recruiter_data.organisation_email,)
    if existing_email: raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Organisation email already registered",)
    existing_mobile = get_recruiter_by_mobile(db, recruiter_data.mobile_number,)
    if existing_mobile: raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mobile number already registered",)
    recruiter = create_recruiter(db, recruiter_data,)
    return recruiter

@router.post("/login", response_model=TokenResponse,)
def login_recruiter(login_data: RecruiterLogin, db: Session = Depends(get_db),):
    recruiter = get_recruiter_by_email(db, login_data.organisation_email,)
    if recruiter is None: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password",)
    password_is_valid = verify_password(login_data.password, recruiter.hashed_password,)
    if not password_is_valid: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password",)
    access_token = create_access_token(subject=str(recruiter.recruiter_id))
    return TokenResponse(access_token=access_token, token_type="bearer",)

@router.get("/profile", response_model=RecruiterResponse,)
def get_my_profile(current_recruiter: Recruiter = Depends(get_current_recruiter),):
    return current_recruiter

@router.get(
    "/jobs/{job_id}/applications",
    response_model=list[RecruiterApplicationResponse],
)
def view_job_applications(
    job_id: int,
    current_recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db),
):
    return get_job_applications(
        db=db,
        recruiter_id=current_recruiter.recruiter_id,
        job_id=job_id,
    )

@router.put(
    "/applications/{application_id}/status",
    response_model=ApplicationResponse,
)
def change_application_status(
    application_id: int,
    payload: ApplicationStatusUpdate,
    current_recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db),
):
    return update_application_status(
        db=db,
        recruiter_id=current_recruiter.recruiter_id,
        application_id=application_id,
        new_status=payload.status,
    )

@router.post(
    "/applications/{application_id}/notes",
    response_model=ApplicationNoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application_note(
    application_id: int,
    payload: ApplicationNoteCreate,
    current_recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db),
):
    return add_application_note(
        db=db,
        recruiter_id=current_recruiter.recruiter_id,
        application_id=application_id,
        notes=payload.notes,
    )


@router.get(
    "/applications/{application_id}/notes",
    response_model=list[ApplicationNoteResponse],
)
def view_application_notes(
    application_id: int,
    current_recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db),
):
    return get_application_notes(
        db=db,
        recruiter_id=current_recruiter.recruiter_id,
        application_id=application_id,
    )

@router.get(
    "/applications/{application_id}/resume",
)
def view_application_resume(
    application_id: int,
    current_recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db),
):
    return get_application_resume(
        db=db,
        recruiter_id=current_recruiter.recruiter_id,
        application_id=application_id,
    )