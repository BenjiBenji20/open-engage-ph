import uuid
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from ..enums.oauth_provider import OAuthProvider


class UserOAuth(Base):
  __tablename__ = "user_oauth"

  id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  provider = Column(Enum(OAuthProvider), default=OAuthProvider.GOOGLE, nullable=False)   
  provider_user_id = Column(String, nullable=False, unique=True)  # unique ID from provider
  access_token = Column(String)
  refresh_token = Column(String)

  # Polymorphic foreign keys
  end_user_id = Column(
    String(36), 
    ForeignKey("end_user.id", ondelete="CASCADE"), 
    nullable=True,
    unique=True, # for 1-to-1 rs
    index=True
  )
  admin_id = Column(
    String(36), 
    ForeignKey("admin.id", ondelete="CASCADE"), 
    nullable=True,
    unique=True, # for 1-to-1 rs
    index=True
  )
  moderator_id = Column(
    String(36), 
    ForeignKey("moderator.id", ondelete="CASCADE"), 
    nullable=True,
    unique=True, # for 1-to-1 rs
    index=True
  )
  regulator_id = Column(
    String(36), 
    ForeignKey("regulator.id", ondelete="CASCADE"), 
    nullable=True,
    unique=True, # for 1-to-1 rs
    index=True
  )
  
  # relationships
  end_user = relationship("EndUser", back_populates="oauth_account")
  admin = relationship("Admin", back_populates="oauth_account")
  moderator = relationship("Moderator", back_populates="oauth_account")
  regulator = relationship("Regulator", back_populates="oauth_account")
  