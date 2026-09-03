from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.mixins import TimestampMixin

class Candidate(TimestampMixin, Base):
    __tablename__ = "candidates"
    
    candidate_id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    name: Mapped[str] = mapped_column(String(100), nullable=False,)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False,)
    hashed_password: Mapped[str] = mapped_column(String(255),nullable=False,)
    mobile_number: Mapped[str] = mapped_column(String(15), unique=True, nullable=False,)
    is_verified: Mapped[bool] = mapped_column(Boolean,default=False,nullable=False,)

    details = relationship("CandidateDetails", back_populates="candidate", uselist=False, cascade="all, delete-orphan",)
