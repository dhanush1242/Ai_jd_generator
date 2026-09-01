from pydantic import BaseModel, ConfigDict

class CandidateDetailsCreate(BaseModel):
    education_qualification: str | None = None
    passedout_year: int | None = None
    experience: str | None = None
    skills: str | None = None
    preferred_work_mode: str | None = None
    preferred_job_type: str | None = None
    preferred_work_location: str | None = None
    profile_picture: str | None = None
    resume: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None

class CandidateDetailsResponse(BaseModel):
    candidate_details_id: int
    candidate_id: int
    education_qualification: str | None
    passedout_year: int | None
    experience: str | None
    skills: str | None
    preferred_work_mode: str | None
    preferred_job_type: str | None
    preferred_work_location: str | None
    profile_picture: str | None
    resume: str | None
    github_url: str | None
    linkedin_url: str | None

    model_config = ConfigDict(from_attributes=True)