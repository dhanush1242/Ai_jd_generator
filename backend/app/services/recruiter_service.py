from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.recruiter import Recruiter
from app.schemas.recruiter import RecruiterCreate


def get_recruiter_by_email(
    db: Session,
    email: str,
) -> Recruiter | None:

    statement = select(Recruiter).where(
        Recruiter.organisation_email == email
    )

    return db.scalar(statement)


def get_recruiter_by_mobile(
    db: Session,
    mobile_number: str,
) -> Recruiter | None:

    statement = select(Recruiter).where(
        Recruiter.mobile_number == mobile_number
    )

    return db.scalar(statement)


def create_recruiter(
    db: Session,
    recruiter_data: RecruiterCreate,
) -> Recruiter:

    recruiter = Recruiter(
        name=recruiter_data.name,
        mobile_number=recruiter_data.mobile_number,
        organisation_email=recruiter_data.organisation_email,
        hashed_password=hash_password(
            recruiter_data.password
        ),
    )

    db.add(recruiter)

    db.commit()

    db.refresh(recruiter)

    return recruiter