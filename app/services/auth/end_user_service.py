from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.customed_exceptions import (
  DuplicateEntryException, ResourceNotFoundException,
  InternalServerError, UnauthorizedAccessException,
)
from app.schemas.end_user.end_user_schema import EUReqRegistrationSchema, EUResRegistrationSchema
from app.models.end_user.end_user import EndUser
from app.utils.db_look_up_utils import get_user_by_email
from app.utils.user_validation_utils import hash_password, validate_password
from app.configs.settings import settings
from app.dependencies.oauth_uri import end_user_oauth2_scheme

import logging

logger = logging.getLogger(__name__)

async def end_user_registration_service(
  user: EUReqRegistrationSchema, 
  db: AsyncSession
) -> EUResRegistrationSchema:
  "handles end user registration logic"
  try:
    # validate user by search to its email
    user_in_db = await get_user_by_email(
      model=EndUser,
      email=user.email,
      db=db
    )
    
    # if user already existed, invalidate the registration
    if user_in_db:
      raise DuplicateEntryException(f"User with {user.email} as email already exists.")
    
    hashed_pw = hash_password(user.password)
    
    user_dict = user.model_dump(exclude={"password"})  
    user_dict["password_hash"] = hashed_pw 

    user_db = EndUser(**user_dict) 
    db.add(user_db)
    await db.commit()
    await db.refresh(user_db)

    return user_db
  except DuplicateEntryException:
    raise 
  except Exception as e:
    logger.error(f"An error occured: {e}")
    raise InternalServerError("An expected error occured.")
  

async def end_user_auth_token_service(email: str, password: str, db: AsyncSession) -> EndUser:
  user: EndUser = await get_user_by_email(model=EndUser, email=email, db=db)
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
  