from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Candidate(Base):
    __tablename__ = "candidates"
    
    candidate_id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    name: Mapped[str] = mapped_column(String(100), nullable=False,)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False,)
    hashed_password: Mapped[str] = mapped_column(String(255),nullable=False,)
    mobile_number: Mapped[str] = mapped_column(String(15), unique=True, nullable=False,)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False,)
    is_verified: Mapped[bool] = mapped_column(Boolean,default=False,nullable=False,)

    details = relationship("CandidateDetails", back_populates="candidate", uselist=False, cascade="all, delete-orphan",)
