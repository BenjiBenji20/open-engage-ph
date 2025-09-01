import uuid
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from ..enums.oauth_provider import OAuthProvider


class UserOAuth(Base):
  __tablename__ = "user_oauth"

  id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  provider = Column(Enum(OAuthProvider), default=OAuthProvider.GOOGLE, nullable=False)   
  provider_user_id = Column(String, nullable=False)  # unique ID from provider
  access_token = Column(String)
  refresh_token = Column(String)

  # Polymorphic foreign keys
  end_user_id = Column(String(36), ForeignKey("end_user.id"), nullable=True)
  admin_id = Column(String(36), ForeignKey("admin.id"), nullable=True)
  moderator_id = Column(String(36), ForeignKey("moderator.id"), nullable=True)
  regulator_id = Column(String(36), ForeignKey("regulator.id"), nullable=True)
  
  # relationships
  end_user = relationship("EndUser", back_populates="oauth_accounts")
  admin = relationship("Admin", back_populates="oauth_accounts")
  moderator = relationship("Moderator", back_populates="oauth_accounts")
  regulator = relationship("Regulator", back_populates="oauth_accounts")
  