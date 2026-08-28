from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RecruiterCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    mobile_number: str = Field(
        min_length=10,
        max_length=15,
    )

    organisation_email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class RecruiterResponse(BaseModel):
    recruiter_id: int
    name: str
    mobile_number: str
    organisation_email: EmailStr
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )