from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ApplicationNote(Base):
    __tablename__ = "application_notes"

    note_id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    application_id: Mapped[int] = mapped_column(
        ForeignKey(
            "applications.application_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    recruiter_id: Mapped[int] = mapped_column(
        ForeignKey(
            "recruiters.recruiter_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    notes: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    application = relationship("Application")
    recruiter = relationship("Recruiter")