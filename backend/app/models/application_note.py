from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.mixins import TimestampMixin

class ApplicationNote(TimestampMixin, Base):
    __tablename__ = "application_notes"

    note_id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.application_id", ondelete="CASCADE",), nullable=False, index=True,)
    recruiter_id: Mapped[int] = mapped_column(ForeignKey("recruiters.recruiter_id", ondelete="CASCADE",), nullable=False, index=True,)
    notes: Mapped[str] = mapped_column(Text, nullable=False,)

    application = relationship("Application")
    recruiter = relationship("Recruiter")