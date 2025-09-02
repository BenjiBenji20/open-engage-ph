from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..enums.user_role import ModelRole
from app.models.base_user import BaseUser
from app.db.base import Base

class Moderator(BaseUser, Base):
  __tablename__ = "moderator"
  
  # This ensures proper inheritance mapping
  __mapper_args__ = {
    'polymorphic_identity': ModelRole.MODERATOR,
    'polymorphic_on': BaseUser.role
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
  