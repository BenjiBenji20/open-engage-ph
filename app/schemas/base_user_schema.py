from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, field_validator, EmailStr

import regex

from app.exceptions.customed_exceptions import UnprocessibleContentException
from app.models.enums.user_role import ModelRole


class BaseUserResponseSchema(BaseModel):
  id: str
  created_at: datetime
  
  email: str
  username: str
  role: ModelRole
  
  complete_name: str
  complete_address: str
  age: int
  
  class Config: 
    from_attributes = True
    
    
class BaseUserRequestSchema(BaseModel):
  email: EmailStr = Field(..., description="Valid email address")
  username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]{3,20}$")
  password: str = Field(..., min_length=8, max_length=50)
  role: ModelRole = ModelRole.END_USER
  
  complete_name: str = Field(..., max_length=50)
  complete_address: str = Field(default="Malabon City", max_length=100)
  age: int = Field(default=18, gt=0, le=120)
  
  profile_photo_url: str | None = Field(None, max_length=255)
  profile_photo_filename: str | None = Field(None, max_length=255)

  @field_validator("complete_name")
  @classmethod
  def validate_name(cls, val):
    # Names should start with a letter, contain only letters, spaces, hyphens, apostrophes
    pattern = r"^[\p{L}][\p{L}\p{M}'\- ]*$"
    if not regex.match(pattern, val.strip()):
      raise UnprocessibleContentException(f"Must be valid name format: {val}")
    return val.strip()

  @field_validator("complete_address")
  @classmethod
  def validate_address(cls, val):
    # Addresses can start with numbers, contain letters, numbers, spaces, punctuation
    pattern = r"^[\p{L}\p{N}][\p{L}\p{N}\p{M}'\-\s.,#]*$"
    if not regex.match(pattern, val.strip()):
      raise UnprocessibleContentException(f"Must be valid address format: {val}")
    return val.strip()
  
  @field_validator('email')
  @classmethod
  def validate_email_length(cls, v):
    """Additional length validation for database compatibility"""
    if len(v) > 100:
      raise ValueError('Email must be less than 100 characters')
    return v.lower().strip()
  