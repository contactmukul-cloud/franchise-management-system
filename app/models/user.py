from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)

    role = Column(String, nullable=False)  # super_admin / franchise

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)