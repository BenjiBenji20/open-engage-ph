from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_session import get_async_db
from app.schemas.end_user.end_user_schema import EUReqRegistrationSchema, EUResRegistrationSchema
from app.exceptions.customed_exceptions import UnprocessibleContentException, InvalidRequestException
from app.services.auth.end_user_service import end_user_registration_service

end_user_router = APIRouter(
  prefix="/api/enduser",
  tags=["end user API endpoints"]
)

@end_user_router.post("/registration", response_model=EUResRegistrationSchema)
async def end_user_registration_router(user: EUReqRegistrationSchema, db: AsyncSession = Depends(get_async_db)):
  try:
    new_user: EUResRegistrationSchema = await end_user_registration_service(user, db)
    
    if not new_user:
      raise UnprocessibleContentException("Value error")
    
    return new_user
  except Exception as e:
    raise InvalidRequestException("Invalid user registration")
  
  