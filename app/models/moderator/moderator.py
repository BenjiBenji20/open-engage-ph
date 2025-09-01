from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..enums.role import ModelRole
from app.models.base_user import BaseUser

class Moderator(BaseUser):
  __tablename__ = "moderator"
  
  # This ensures proper inheritance mapping
  __mapper_args__ = {
    'polymorphic_identity': ModelRole.MODERATOR,
    'polymorphic_on': BaseUser.role
  }
  
  post_photos = Column(String, nullable=True)
  post_photos_filename = Column(String, nullable=True)
  
  # relationships
  photos = relationship("UserPhoto", back_populates="moderator")
  oauth_accounts = relationship("UserOAuth", back_populates="moderator")
  