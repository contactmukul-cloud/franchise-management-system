from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.models.franchise import Franchise
from app.core.security import hash_password


def create_franchise(db: Session, data):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    existing_code = db.query(Franchise).filter(Franchise.franchise_code == data.franchise_code).first()
    if existing_code:
        raise HTTPException(status_code=400, detail="Franchise code already exists")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        phone=data.phone,
        address=data.address,
        role="franchise",
        is_active=True,
        is_verified=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    franchise = Franchise(
        user_id=user.id,
        franchise_code=data.franchise_code,
        status="active"
    )

    db.add(franchise)
    db.commit()

    return {"message": "Franchise created successfully"}


def get_all_franchises(db: Session, page: int = 1, limit: int = 10, search: str = None, status: str = None):
    query = db.query(User, Franchise).join(Franchise, User.id == Franchise.user_id).filter(User.role == "franchise")

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (User.name.ilike(search_term)) |
            (User.email.ilike(search_term)) |
            (User.phone.ilike(search_term)) |
            (Franchise.franchise_code.ilike(search_term))
        )

    if status:
        query = query.filter(Franchise.status == status)

    total = query.count()
    records = query.offset((page - 1) * limit).limit(limit).all()

    result = []
    for user, franchise in records:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "role": user.role,
            "franchise_code": franchise.franchise_code,
            "status": franchise.status
        })

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": result
    }


def get_franchise_by_id(db: Session, franchise_id: int):
    record = db.query(User, Franchise).join(Franchise, User.id == Franchise.user_id).filter(
        User.id == franchise_id,
        User.role == "franchise"
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Franchise not found")

    user, franchise = record

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "address": user.address,
        "role": user.role,
        "franchise_code": franchise.franchise_code,
        "status": franchise.status
    }


def update_franchise(db: Session, franchise_id: int, data):
    record = db.query(User, Franchise).join(Franchise, User.id == Franchise.user_id).filter(
        User.id == franchise_id,
        User.role == "franchise"
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Franchise not found")

    user, franchise = record

    if data.name is not None:
        user.name = data.name

    if data.phone is not None:
        user.phone = data.phone

    if data.address is not None:
        user.address = data.address

    if data.status is not None:
        franchise.status = data.status

    db.commit()
    db.refresh(user)
    db.refresh(franchise)

    return {
        "message": "Franchise updated successfully",
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "role": user.role,
            "franchise_code": franchise.franchise_code,
            "status": franchise.status
        }
    }


def delete_franchise(db: Session, franchise_id: int):
    user = db.query(User).filter(
        User.id == franchise_id,
        User.role == "franchise"
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Franchise not found")

    db.delete(user)
    db.commit()

    return {"message": "Franchise deleted successfully"}