from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from ..enums.user_role import ModelRole
from app.models.base_user import BaseUser

class Regulator(BaseUser, Base):
  __tablename__ = "regulator"
  
  # This ensures proper inheritance mapping
  __mapper_args__ = {
    'polymorphic_identity': ModelRole.REGULATOR,
    'polymorphic_on': BaseUser.role
  }
  
  post_photos = Column(String, nullable=True)
  post_photos_filename = Column(String, nullable=True)
  
  # relationships
  photos = relationship("UserPhoto", back_populates="regulator")
  oauth_account = relationship(
    "UserOAuth", 
    back_populates="regulator",
    uselist=False,
    cascade="all, delete-orphan",
    doc="One oauth acc only per user"
  )
  updated_ordinance = relationship(
    "Ordinance",
    back_populates="regulator",
    uselist=True, 
    doc="many ordinance can be updated by one regulator user"
  )