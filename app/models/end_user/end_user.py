from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from ..enums.user_role import ModelRole
from app.models.base_user import BaseUser

class EndUser(BaseUser):
  __tablename__ = "end_user"
  
  id = Column(String(36), ForeignKey("base_users.id"), primary_key=True)
  
  # This ensures proper inheritance mapping
  __mapper_args__ = {
    'polymorphic_identity': ModelRole.END_USER
  }
  
  # anonimity
  is_anonymous = Column(Boolean, default=False, nullable=False)
  
  # relationships
  photos = relationship("UserPhoto", back_populates="end_user")
  oauth_account = relationship(
    "UserOAuth", 
    back_populates="end_user",
    uselist=False,
    cascade="all, delete-orphan",
    doc="One oauth acc only per user"
  )
  