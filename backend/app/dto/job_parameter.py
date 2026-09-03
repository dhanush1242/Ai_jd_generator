from pydantic import BaseModel, ConfigDict, Field

class JobParameterCreate(BaseModel):
    job_title: str = Field(min_length=2, max_length=150,)
    required_skills: str = Field(min_length=2, max_length=1000,)
    education_qualification: str = Field(min_length=2, max_length=255,)
    experience: str = Field(min_length=1, max_length=100,)
    location: str = Field(min_length=2, max_length=255,)
    passedout_year: int | None = None
    work_mode: str = Field(min_length=2, max_length=50,)
    job_type: str = Field(min_length=2, max_length=50,)
    package: str | None = Field(default=None, max_length=100,)

class JobParameterResponse(BaseModel):
    job_id: int
    recruiter_id: int
    job_title: str
    required_skills: str
    education_qualification: str
    experience: str
    location: str
    passedout_year: int | None
    work_mode: str
    job_type: str
    package: str | None

    model_config = ConfigDict(from_attributes=True)

class JobParameterUpdate(BaseModel):
    job_title: str | None = None
    required_skills: str | None = None
    education_qualification: str | None = None
    experience: str | None = None
    location: str | None = None
    passedout_year: int | None = None
    work_mode: str | None = None
    job_type: str | None = None
    package: str | None = None