from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ..enums.user_role import ModelRole
from app.models.base_user import BaseUser

class Regulator(BaseUser):
  __tablename__ = "regulator"
  
  id = Column(String(36), ForeignKey("base_users.id"), primary_key=True)
  
  # This ensures proper inheritance mapping
  __mapper_args__ = {
    'polymorphic_identity': ModelRole.REGULATOR
  }
  
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