from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Application(Base):
    __tablename__ = "applications"

    __table_args__ = (
        UniqueConstraint(
            "candidate_id",
            "job_id",
            name="uq_candidate_job_application",
        ),
    )

    application_id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey(
            "candidates.candidate_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey(
            "job_parameters.job_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    jd_id: Mapped[int] = mapped_column(
        ForeignKey(
            "job_descriptions.jd_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    resume_url: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="applied",
        server_default="applied",
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

    candidate = relationship("Candidate")

    job = relationship("JobParameter")

    jd = relationship("JobDescription")