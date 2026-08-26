from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    jd_id: Mapped[int] = mapped_column(
        primary_key=True,
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

    generated_jd: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    updated_jd: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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

    job = relationship(
        "JobParameter",
        back_populates="job_descriptions",
    )