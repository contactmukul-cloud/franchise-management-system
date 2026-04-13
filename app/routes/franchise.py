from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.franchise import FranchiseCreate, FranchiseUpdate
from app.services.franchise_service import (
    create_franchise,
    get_all_franchises,
    get_franchise_by_id,
    update_franchise,
    delete_franchise
)
from app.dependencies.role_checker import require_super_admin

router = APIRouter()


@router.post("/")
def create_franchise_api(
    data: FranchiseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin)
):
    return create_franchise(db, data)


@router.get("/")
def get_franchise_list_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = None,
    status: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin)
):
    return get_all_franchises(db, page, limit, search, status)


@router.get("/{franchise_id}")
def get_franchise_by_id_api(
    franchise_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin)
):
    return get_franchise_by_id(db, franchise_id)


@router.put("/{franchise_id}")
def update_franchise_api(
    franchise_id: int,
    data: FranchiseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin)
):
    return update_franchise(db, franchise_id, data)


@router.delete("/{franchise_id}")
def delete_franchise_api(
    franchise_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin)
):
    return delete_franchise(db, franchise_id)