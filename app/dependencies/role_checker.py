from fastapi import Depends, HTTPException
from app.dependencies.auth import get_current_user


def require_super_admin(current_user=Depends(get_current_user)):
    if current_user.role.strip().lower() != "super_admin":
        raise HTTPException(status_code=403, detail="Only super admin can access this")
    return current_user