from sqlalchemy import Column, String, DateTime, Boolean, Integer, Enum
from datetime import datetime, timezone
import uuid

from app.models.enums.user_role import ModelRole
from app.db.base import Base

class BaseUser(Base):
  __tablename__ = "base_users"
  
  id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
  
  # account details
  email = Column(String(100), nullable=False, unique=True, index=True)
  username = Column(String(50), nullable=False, unique=True)
  password_hash = Column(String(100), nullable=True)
  role = Column(Enum(ModelRole), nullable=False)
  
  # personal details
  complete_name = Column(String(50), nullable=False)
  complete_address = Column(String(50), nullable=False)
  age = Column(Integer, default=18, nullable=False)
  
  # account guard
  failed_attempts = Column(Integer, default=0, nullable=False)
  banned_until = Column(DateTime(timezone=True), nullable=True)
  last_login = Column(DateTime(timezone=True), nullable=True)
  is_active = Column(Boolean, default=False, nullable=False)
  
  __mapper_args__ = {
    "polymorphic_on": role
  }
  