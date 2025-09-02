from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base
from ..enums.user_role import ModelRole
from app.models.base_user import BaseUser

class EndUser(BaseUser, Base):
  __tablename__ = "end_user"
  
  # This ensures proper inheritance mapping
  __mapper_args__ = {
    'polymorphic_identity': ModelRole.END_USER,
    'polymorphic_on': BaseUser.role
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
  