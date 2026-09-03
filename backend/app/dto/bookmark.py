from datetime import datetime
from pydantic import BaseModel

class BookmarkResponse(BaseModel):
    bookmark_id: int
    candidate_id: int
    job_id: int
    created_at: datetime

    model_config = {"from_attributes": True}