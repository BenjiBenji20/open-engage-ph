from datetime import datetime, timedelta, timezone
from jose import JWTError
import jwt

from app.configs.settings import settings
from app.exceptions.customed_exceptions import UnauthorizedAccessException


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