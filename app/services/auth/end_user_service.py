from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.customed_exceptions import DuplicateEntryException, InternalServerError
from app.schemas.end_user.end_user_schema import EUReqRegistrationSchema, EUResRegistrationSchema
from app.models.end_user.end_user import EndUser
from app.utils.db_look_up_utils import get_user_by_email
from app.utils.user_validation_utils import hash_password

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
  