from datetime import datetime
from pydantic import BaseModel

class ApplicationResponse(BaseModel):
    application_id: int
    candidate_id: int
    job_id: int
    jd_id: int
    resume_url: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class RecruiterApplicationResponse(BaseModel):
    application_id: int
    candidate_id: int
    candidate_name: str
    candidate_email: str
    mobile_number: str
    education_qualification: str | None
    passedout_year: int | None
    experience: str | None
    skills: str | None
    resume_url: str
    github_url: str | None
    linkedin_url: str | None
    job_id: int
    jd_id: int
    status: str
    created_at: datetime
    updated_at: datetime

class ApplicationStatusUpdate(BaseModel):
    status: str

class CandidateApplicationResponse(BaseModel):
    application_id: int
    job_id: int
    jd_id: int
    job_title: str
    location: str
    experience: str
    work_mode: str
    job_type: str
    package: str | None
    status: str
    created_at: datetime
    updated_at: datetime