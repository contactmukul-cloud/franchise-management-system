from pydantic import BaseModel, EmailStr
from typing import Optional


class FranchiseCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    address: str
    franchise_code: str


class FranchiseUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None