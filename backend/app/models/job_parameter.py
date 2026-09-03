from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class JobParameter(Base):
    __tablename__ = "job_parameters"
    
    job_id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    recruiter_id: Mapped[int] = mapped_column(ForeignKey("recruiters.recruiter_id", ondelete="CASCADE",), nullable=False, index=True,)
    job_title: Mapped[str] = mapped_column(String(150), nullable=False,)
    required_skills: Mapped[str] = mapped_column(String(1000),nullable=False,)
    education_qualification: Mapped[str] = mapped_column(String(255),nullable=False,)
    experience: Mapped[str] = mapped_column(String(100), nullable=False,)
    location: Mapped[str] = mapped_column(String(255), nullable=False,)
    passedout_year: Mapped[int | None] = mapped_column(Integer, nullable=True,)
    work_mode: Mapped[str] = mapped_column(String(50), nullable=False,)
    job_type: Mapped[str] = mapped_column(String(50), nullable=False,)
    package: Mapped[str | None] = mapped_column(String(100), nullable=True,)
    recruiter = relationship("Recruiter", back_populates="jobs",)

    job_descriptions = relationship("JobDescription", back_populates="job", cascade="all, delete-orphan",)