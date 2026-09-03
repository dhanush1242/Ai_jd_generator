from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    __table_args__ = (UniqueConstraint("candidate_id", "job_id", name="uq_candidate_job_bookmark",),)

    bookmark_id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.candidate_id", ondelete="CASCADE",), nullable=False, index=True,)
    job_id: Mapped[int] = mapped_column(ForeignKey("job_parameters.job_id", ondelete="CASCADE",), nullable=False, index=True,)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)

    candidate = relationship("Candidate")
    job = relationship("JobParameter")