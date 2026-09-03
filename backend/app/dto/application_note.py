from datetime import datetime
from pydantic import BaseModel

class ApplicationNoteCreate(BaseModel):
    notes: str

class ApplicationNoteResponse(BaseModel):
    note_id: int
    application_id: int
    recruiter_id: int
    notes: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}