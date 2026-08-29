import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.db.dependencies import get_db
from app.models.recruiter import Recruiter
from app.models.candidate import Candidate

bearer_scheme = HTTPBearer()

def get_current_recruiter(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db),) -> Recruiter:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        recruiter_id = payload.get("sub")
        if recruiter_id is None: raise credentials_exception
        recruiter_id = int(recruiter_id)
    except(jwt.InvalidTokenError, ValueError,): raise credentials_exception
    recruiter = db.get(Recruiter, recruiter_id,)
    if recruiter is None: raise credentials_exception
    return recruiter

def get_current_candidate(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db),) -> Candidate:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        candidate_id = payload.get("sub")
        if candidate_id is None: raise credentials_exception
        candidate_id = int(candidate_id)
    except(jwt.InvalidTokenError, ValueError,): raise credentials_exception
    candidate = db.get(Candidate, candidate_id,)
    if candidate is None: raise credentials_exception
    return candidate