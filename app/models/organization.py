# app/models/organization.py
from sqlalchemy import Column, Integer, String, DateTime, func
from app.models.base import Base


class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True, index=True)
    org_name = Column(String(255))
    org_status = Column(String(10))
    is_deleted = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

