# models/photo.py
from datetime import datetime, timezone
import uuid
from sqlalchemy import VARCHAR, Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class UserPhoto(Base):
  __tablename__ = "user_photos"

  id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

  # Photo storage info
  filename = Column(String, nullable=False)
  file_url = Column(String, nullable=True)  # CDN or storage URL
  file_size = Column(Integer, nullable=True)  # Size in bytes
  mime_type = Column(String, nullable=True)  # image/jpeg, image/png
  
  # Metadata
  uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
  is_profile_photo = Column(Boolean, default=False)
  
  title = Column(VARCHAR(50), nullable=True)
  description = Column(VARCHAR(255), nullable=True)
  
  # Polymorphic foreign keys
  end_user_id = Column(String(36), ForeignKey("end_user.id"), nullable=True)
  admin_id = Column(String(36), ForeignKey("admin.id"), nullable=True)
  moderator_id = Column(String(36), ForeignKey("moderator.id"), nullable=True)
  regulator_id = Column(String(36), ForeignKey("regulator.id"), nullable=True)
  
  # Relationship
  end_user = relationship("EndUser", back_populates="photos")
  admin = relationship("Admin", back_populates="photos")
  moderator = relationship("Moderator", back_populates="photos")
  regulator = relationship("Regulator", back_populates="photos")
  