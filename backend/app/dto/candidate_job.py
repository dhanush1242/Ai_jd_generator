from datetime import datetime
from pydantic import BaseModel

class CandidateJobResponse(BaseModel):
    job_id: int
    job_title: str
    required_skills: str
    education_qualification: str
    experience: str
    location: str
    passedout_year: int | None
    work_mode: str
    job_type: str
    package: str | None
    jd_id: int
    version_number: int
    job_description: str
    published_at: datetime | None