from pydantic import BaseModel, EmailStr


class RecruiterLogin(BaseModel):
    organisation_email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str