from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ..enums.user_role import ModelRole
from app.models.base_user import BaseUser
from app.db.base import Base

class Moderator(BaseUser):
  __tablename__ = "moderator"
  
  id = Column(String(36), ForeignKey("base_users.id"), primary_key=True)
  
  # This ensures proper inheritance mapping
  __mapper_args__ = {
    'polymorphic_identity': ModelRole.MODERATOR
  }
  
  # relationships
  photos = relationship("UserPhoto", back_populates="moderator")
  oauth_account = relationship(
    "UserOAuth", 
    back_populates="moderator",
    uselist=False,
    cascade="all, delete-orphan",
    doc="One oauth acc only per user"
  )
  