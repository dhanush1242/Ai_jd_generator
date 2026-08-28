from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CandidateCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100,
    )

    mobile_number: str = Field(
        min_length=10,
        max_length=15,
    )


class CandidateResponse(BaseModel):
    candidate_id: int
    name: str
    email: EmailStr
    mobile_number: str
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class CandidateLogin(BaseModel):
    email: EmailStr
    password: str