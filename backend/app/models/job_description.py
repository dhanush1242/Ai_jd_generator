from datetime import datetime
from sqlalchemy import (Boolean, DateTime, ForeignKey, Integer, Text, UniqueConstraint,)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.mixins import TimestampMixin

class JobDescription(TimestampMixin, Base):
    __tablename__ = "job_descriptions"

    __table_args__ = (UniqueConstraint("job_id", "version_number", name="uq_job_description_version",),)

    jd_id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    job_id: Mapped[int] = mapped_column(ForeignKey("job_parameters.job_id", ondelete="CASCADE",), nullable=False, index=True,)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False,)
    generated_jd: Mapped[str] = mapped_column(Text, nullable=False,)
    updated_jd: Mapped[str | None] = mapped_column(Text, nullable=True,)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True,)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)

    job = relationship("JobParameter", back_populates="job_descriptions",)