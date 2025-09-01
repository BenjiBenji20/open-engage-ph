from datetime import datetime, timezone
import uuid
from sqlalchemy import VARCHAR, Column, DateTime, Enum, String
from app.db.base import Base
from app.models.enums.ordinance_category import OrdinanceCategory

class Ordinance(Base):
  __tablename__="ordinance"
  
  id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
  updated_at = Column(DateTime(timezone=True), nullable=True)
  created_by = Column(String(50), default="azathoth")
  
  ordinance_number = Column(String(20), nullable=False, unique=True)
  title = Column(VARCHAR(50), nullable=False)
  author = Column(String(50), nullable=False)
  description = Column(VARCHAR(255), nullable=False)
  ai_explanation = Column(VARCHAR(255), nullable=True)
  
  category = Column(Enum(OrdinanceCategory), nullable=False)
  