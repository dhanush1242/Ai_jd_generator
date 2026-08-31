from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class CandidateDetails(Base):
    __tablename__ = "candidate_details"
    
    candidate_details_id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.candidate_id", ondelete="CASCADE",), unique=True, nullable=False, index=True,)
    education_qualification: Mapped[str | None] = mapped_column(String(255), nullable=True,)
    passedout_year: Mapped[int | None] = mapped_column(Integer, nullable=True,)
    experience: Mapped[str | None] = mapped_column(String(100), nullable=True,)
    skills: Mapped[str | None] = mapped_column(Text, nullable=True,)
    preferred_work_mode: Mapped[str | None] = mapped_column(String(50), nullable=True,)
    preferred_job_type: Mapped[str | None] = mapped_column(String(50), nullable=True,)
    preferred_work_location: Mapped[str | None] = mapped_column(String(255), nullable=True,)
    profile_picture: Mapped[str | None] = mapped_column(String(500), nullable=True,)
    resume: Mapped[str | None] = mapped_column(String(500), nullable=True,)
    github_url: Mapped[str | None] = mapped_column(String(500), nullable=True,)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True,)

    candidate = relationship("Candidate", back_populates="details",)