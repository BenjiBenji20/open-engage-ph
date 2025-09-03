from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.configs.settings import settings
from app.exceptions.customed_exceptions import ResourceNotFoundException, UnauthorizedAccessException
from app.utils.db_look_up_utils import get_user_by_email
from app.utils.user_validation_utils import validate_password
from app.models.base_user import BaseUser


import logging

logger = logging.getLogger(__name__)

async def auth_token_service(email: str, password: str, db: AsyncSession) -> Optional[BaseUser]:
  user: Optional[BaseUser] = await get_user_by_email(model=BaseUser, email=email, db=db)
  if not user:
    raise ResourceNotFoundException(f"User with email: {email} not found.")
  
  now = datetime.now(timezone.utc)
  
  # Check if user is banned
  if user.banned_until:
    banned_until_aware = user.banned_until.replace(tzinfo=timezone.utc)
    if banned_until_aware > now:
      raise UnauthorizedAccessException(f"User is banned until {user.banned_until}.")
    
  # if failed attempts persists due to wrong password, increment failed_attempts attribute
  if not validate_password(password, user.password_hash):
    user.failed_attempts += 1

    # Ban user if max attempts reached
    if user.failed_attempts >= settings.MAX_FAILED_ATTEMPTS:
      user.banned_until = now + timedelta(minutes=settings.BAN_DURATION_MINUTES)
      # response ban time in minutes
      ban_duration: timedelta = user.banned_until - now
      ban_minutes = int(ban_duration.total_seconds() / 60)
      user.failed_attempts = 0  # reset to avoid stacking bans
      await db.commit()
      raise UnauthorizedAccessException(f"Banned for {ban_minutes} minutes")

    await db.commit()
    raise UnauthorizedAccessException("Invalid email or password.")
  
  # Reset failed attempts on success
  user.failed_attempts = 0
  user.banned_until = None
  user.last_login = now
  user.is_active = True
  await db.commit()

  return user


def generate_access_token(payload: dict) -> str:
  """Generate short lived token exp: 15 mins"""
  # 15mins access token
  token_expiration = datetime.now(timezone.utc) + timedelta(minutes=15)

  # 7 days refresh token
  payload.update({
    "exp": int(token_expiration.timestamp()),
    "type": "access"
    })
  encoded_jwt = jwt.encode(payload, str(settings.JWT_SECRET_KEY), algorithm=settings.JWT_ALGORITHM)
  return encoded_jwt


def generate_refresh_token(payload: dict) -> str:
  """Generate long live token exp: 7 days"""
  # 7 days refresh token
  token_expiration = datetime.now(timezone.utc) + timedelta(days=7)
  payload.update({
    "exp": int(token_expiration.timestamp()),
    "type": "refresh"
    })
  encoded_jwt = jwt.encode(payload, str(settings.JWT_SECRET_KEY), algorithm=settings.JWT_ALGORITHM)
  return encoded_jwt


def refresh_token(refresh_token: str) -> dict:
  try:
    payload = jwt.decode(refresh_token, str(settings.JWT_SECRET_KEY), algorithms=settings.JWT_ALGORITHM)

    if payload.get("type") != "refresh":
      raise UnauthorizedAccessException("Invalid token type.")

    if datetime.now(timezone.utc).timestamp() > payload["exp"]:
      raise UnauthorizedAccessException("Refresh token expired.")

    email = payload.get("sub")
    if not email:
      raise UnauthorizedAccessException("Invalid refresh token.")

    # Recreate access token only
    new_access_token = generate_access_token({
      "sub": email
    })

    return {
      "access_token": new_access_token,
      "token_type": "bearer"
    }

  except JWTError:
    raise UnauthorizedAccessException("Invalid refresh token.")
  