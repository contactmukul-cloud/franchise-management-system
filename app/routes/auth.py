from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import login_user
from app.schemas.auth import LoginRequest

router = APIRouter()


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(
        db,
        request.email,
        request.password,
        request.franchise_code
    )