from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.dto.admin import (
    AdminCreate,
    AdminLogin,
    AdminResponse,
)

from app.models.admin import Admin

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


# ==================================================
# ADMIN REGISTRATION
# ==================================================

@router.post(
    "/register",
    response_model=AdminResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_admin(
    admin_data: AdminCreate,
    db: Session = Depends(get_db),
):

    existing_admin = (
        db.query(Admin)
        .filter(Admin.email == admin_data.email)
        .first()
    )

    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin email already registered",
        )

    admin = Admin(
        name=admin_data.name,
        email=admin_data.email,
        hashed_password=hash_password(
            admin_data.password
        ),
        is_active=True,
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin


# ==================================================
# ADMIN LOGIN
# ==================================================

@router.post(
    "/login",
    response_model=dict,
)
def login_admin(
    login_data: AdminLogin,
    db: Session = Depends(get_db),
):

    admin = (
        db.query(Admin)
        .filter(Admin.email == login_data.email)
        .first()
    )

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    password_is_valid = verify_password(
        login_data.password,
        admin.hashed_password,
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive",
        )

    access_token = create_access_token(
        subject=str(admin.admin_id),
        role="admin",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }