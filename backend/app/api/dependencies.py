import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.dependencies import get_db

from app.models.recruiter import Recruiter
from app.models.candidate import Candidate
from app.models.admin import Admin


bearer_scheme = HTTPBearer()


# ==================================================
# CURRENT RECRUITER
# ==================================================

def get_current_recruiter(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> Recruiter:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        recruiter_id = payload.get("sub")
        role = payload.get("role")

        if recruiter_id is None:
            raise credentials_exception

        if role != "recruiter":
            raise credentials_exception

        recruiter_id = int(recruiter_id)

    except (
        jwt.InvalidTokenError,
        ValueError,
    ):
        raise credentials_exception

    recruiter = db.get(
        Recruiter,
        recruiter_id,
    )

    if recruiter is None:
        raise credentials_exception

    return recruiter


# ==================================================
# CURRENT CANDIDATE
# ==================================================

def get_current_candidate(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> Candidate:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        candidate_id = payload.get("sub")
        role = payload.get("role")

        if candidate_id is None:
            raise credentials_exception

        if role != "candidate":
            raise credentials_exception

        candidate_id = int(candidate_id)

    except (
        jwt.InvalidTokenError,
        ValueError,
    ):
        raise credentials_exception

    candidate = db.get(
        Candidate,
        candidate_id,
    )

    if candidate is None:
        raise credentials_exception

    return candidate


# ==================================================
# CURRENT ADMIN
# ==================================================

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> Admin:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        admin_id = payload.get("sub")
        role = payload.get("role")

        if admin_id is None:
            raise credentials_exception

        if role != "admin":
            raise credentials_exception

        admin_id = int(admin_id)

    except (
        jwt.InvalidTokenError,
        ValueError,
    ):
        raise credentials_exception

    admin = db.get(
        Admin,
        admin_id,
    )

    if admin is None:
        raise credentials_exception

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive",
        )

    return admin