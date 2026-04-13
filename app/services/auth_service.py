from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.models.franchise import Franchise
from app.core.security import verify_password
from app.utils.jwt import create_access_token, create_refresh_token


def login_user(db: Session, email: str, password: str, franchise_code: str = None):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = (user.role or "").strip().lower()

    if role == "franchise":
        if not franchise_code:
            raise HTTPException(status_code=400, detail="Franchise code required")

        franchise_code = franchise_code.strip()

        franchise = db.query(Franchise).filter(
            Franchise.user_id == user.id,
            Franchise.franchise_code == franchise_code
        ).first()

        if not franchise:
            raise HTTPException(status_code=401, detail="Invalid franchise code")

    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": role
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": role
    }