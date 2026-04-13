from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base


class Franchise(Base):
    __tablename__ = "franchises"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    franchise_code = Column(String, unique=True, nullable=False)
    status = Column(String, default="active")