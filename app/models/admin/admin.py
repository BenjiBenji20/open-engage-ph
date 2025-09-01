from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..enums.role import ModelRole
from app.models.base_user import BaseUser

class Admin(BaseUser):
  __tablename__ = "admin"
  
  # This ensures proper inheritance mapping
  __mapper_args__ = {
    'polymorphic_identity': ModelRole.ADMIN,
    'polymorphic_on': BaseUser.role
  }
  
  # relationships
  photos = relationship("UserPhoto", back_populates="admin")
  oauth_accounts = relationship("UserOAuth", back_populates="admin")
  