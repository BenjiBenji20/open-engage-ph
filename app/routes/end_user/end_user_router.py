from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db.db_session import get_async_db
from app.schemas.end_user.end_user_schema import EndUserRequestSchema, EndUserResponseSchema
from app.exceptions.customed_exceptions import UnprocessibleContentException, InvalidRequestException
from app.services.end_user.end_user_service import end_user_registration_service

end_user_router = APIRouter(
  prefix="/api/enduser",
  tags=["end user API endpoints"]
)


logger = logging.getLogger(__name__)

@end_user_router.post("/registration", response_model=EndUserResponseSchema)
async def end_user_registration_router(user: EndUserRequestSchema, db: AsyncSession = Depends(get_async_db)):
  try:
    new_user: EndUserResponseSchema = await end_user_registration_service(user, db)
    
    if not new_user:
      raise UnprocessibleContentException("Value error")
    
    return new_user
  except Exception as e:
    raise InvalidRequestException("Invalid user registration")
  

from app.dependencies.role_checker import role_required
from app.dependencies.current_user import get_current_user
from app.models.end_user.end_user import EndUser
from app.models.enums.user_role import ModelRole

@end_user_router.get("/get-user", response_model=EndUserResponseSchema)
async def get_end_user(
  user: EndUser = Depends(get_current_user),
  roles = Depends(role_required([ModelRole.END_USER]))
) ->  EndUser:
  return user