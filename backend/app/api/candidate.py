import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from uuid import uuid4
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_candidate
from app.core.security import (create_access_token, verify_password)
from app.db.dependencies import get_db
from app.dto.candidate import (CandidateCreate, CandidateResponse, CandidateLogin,)
from app.dto.auth import TokenResponse
from app.dto.candidate_details import (CandidateDetailsCreate, CandidateDetailsResponse,)
from app.dto.candidate_job import CandidateJobResponse
from app.dto.bookmark import BookmarkResponse
from app.dto.application import (ApplicationResponse, CandidateApplicationResponse,)
from app.dto.chat import ChatResponse, ChatRequest
from app.models.candidate import Candidate
from app.services.candidate_details_service import (create_candidate_details, get_candidate_details,)
from app.services.candidate_job_service import get_published_jobs
from app.services.bookmark_service import (add_bookmark, get_candidate_bookmarks, remove_bookmark,)
from app.services.application_service import (apply_for_job, get_candidate_applications,)
from app.services.candidate_service import (create_candidate, get_candidate_by_email, get_candidate_by_mobile,)
from mcp_client.agent import run_agent

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

@router.get("/profile", response_model=CandidateResponse,)
def get_my_profile(current_candidate: Candidate = Depends(get_current_candidate),):
    return current_candidate

@router.post("/details", response_model=CandidateDetailsResponse, status_code=status.HTTP_201_CREATED,)
def create_my_details(details_data: CandidateDetailsCreate, current_candidate: Candidate = Depends(get_current_candidate), db: Session = Depends(get_db),):
    return create_candidate_details(db=db, details_data=details_data, candidate=current_candidate,)

@router.get("/details", response_model=CandidateDetailsResponse,)
def get_my_details(current_candidate: Candidate = Depends(get_current_candidate), db: Session = Depends(get_db),):
    return get_candidate_details(db=db, candidate=current_candidate,)

@router.put("/details", response_model=CandidateDetailsResponse,)
def update_my_details(
    education_qualification: str | None = Form(None),
    passedout_year: int | None = Form(None),
    experience: str | None = Form(None),
    skills: str | None = Form(None),
    preferred_work_mode: str | None = Form(None),
    preferred_job_type: str | None = Form(None),
    preferred_work_location: str | None = Form(None),
    github_url: str | None = Form(None),
    linkedin_url: str | None = Form(None),
    profile_picture: UploadFile | None = File(None),
    resume: UploadFile | None = File(None),
    current_candidate: Candidate = Depends(get_current_candidate), db: Session = Depends(get_db),):
    details = get_candidate_details(db=db, candidate=current_candidate,)

    if education_qualification is not None: details.education_qualification = education_qualification
    if passedout_year is not None: details.passedout_year = passedout_year
    if experience is not None: details.experience = experience
    if skills is not None: details.skills = skills
    if preferred_work_mode is not None: details.preferred_work_mode = preferred_work_mode
    if preferred_job_type is not None: details.preferred_job_type = preferred_job_type
    if preferred_work_location is not None: details.preferred_work_location = preferred_work_location
    if github_url is not None: details.github_url = github_url
    if linkedin_url is not None: details.linkedin_url = linkedin_url

    # Profile picture upload
    if profile_picture:
        allowed_image_types = ["image/jpeg", "image/png",]
        if profile_picture.content_type not in allowed_image_types: raise HTTPException(status_code=400, detail="Profile picture must be JPG or PNG",)
        os.makedirs("uploads/profile_pictures", exist_ok=True,)
        extension = os.path.splitext(profile_picture.filename)[1] # type: ignore
        filename = (
            f"{current_candidate.candidate_id}_" 
            f"{uuid4().hex}{extension}")

        file_path = os.path.join("uploads/profile_pictures", filename,)
        with open(file_path, "wb") as buffer: shutil.copyfileobj(profile_picture.file, buffer,)
        details.profile_picture = file_path

    # Resume upload
    if resume:
        if resume.content_type != "application/pdf":raise HTTPException(status_code=400, detail="Resume must be a PDF file",)
        os.makedirs("uploads/resumes", exist_ok=True,)
        filename = (
            f"{current_candidate.candidate_id}_"
            f"{uuid4().hex}.pdf"
        )
        file_path = os.path.join("uploads/resumes", filename,)
        with open(file_path, "wb") as buffer: shutil.copyfileobj(resume.file,buffer,)
        details.resume = file_path
    db.commit()
    db.refresh(details)
    return details

@router.get("/jobs", response_model=list[CandidateJobResponse],)
def get_candidate_jobs(
    location: str | None = None,
    experience: str | None = None,
    skills: str | None = None,
    current_candidate: Candidate = Depends(get_current_candidate),
    db: Session = Depends(get_db),
):
    return get_published_jobs(db=db, location=location, experience=experience, skills=skills,)

@router.post("/jobs/{job_id}/bookmark", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED,)
def bookmark_job(job_id: int, current_candidate: Candidate = Depends(get_current_candidate), db: Session = Depends(get_db),):
    return add_bookmark(db=db, candidate_id=current_candidate.candidate_id, job_id=job_id,)

@router.get("/bookmarks", response_model=list[BookmarkResponse],)
def get_my_bookmarks(current_candidate: Candidate = Depends(get_current_candidate), db: Session = Depends(get_db),):
    return get_candidate_bookmarks(db=db, candidate_id=current_candidate.candidate_id,)

@router.delete("/jobs/{job_id}/bookmark",)
def delete_bookmark(job_id: int, current_candidate: Candidate = Depends(get_current_candidate), db: Session = Depends(get_db),):
    return remove_bookmark(db=db, candidate_id=current_candidate.candidate_id, job_id=job_id,)

@router.post("/jobs/{job_id}/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED,)
def apply_job(job_id: int, current_candidate: Candidate = Depends(get_current_candidate), db: Session = Depends(get_db),):
    return apply_for_job(db=db, candidate_id=current_candidate.candidate_id, job_id=job_id,)

@router.get("/applications", response_model=list[CandidateApplicationResponse],)
def get_my_applications(current_candidate: Candidate = Depends(get_current_candidate), db: Session = Depends(get_db),):
    return get_candidate_applications(db=db, candidate_id=current_candidate.candidate_id,)

@router.post("/chat", response_model=ChatResponse,)
async def candidate_chat(request: ChatRequest, current_candidate: Candidate = Depends(get_current_candidate),):
    response = await run_agent(user_message=request.message, role="candidate", user_id=current_candidate.candidate_id,)
    return ChatResponse(response=response)