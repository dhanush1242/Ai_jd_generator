from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class JobDescriptionUpdate(BaseModel):
    updated_jd: str = Field(
        min_length=1,
    )


class JobDescriptionResponse(BaseModel):
    jd_id: int
    job_id: int
    version_number: int
    generated_jd: str
    updated_jd: str | None = None
    is_published: bool
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )
