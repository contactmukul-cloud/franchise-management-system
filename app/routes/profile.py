from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter()


@router.get("/")
def get_profile(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "address": current_user.address,
        "role": current_user.role
    }