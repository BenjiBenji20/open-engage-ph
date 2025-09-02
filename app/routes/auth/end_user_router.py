from fastapi import APIRouter, Depends, Request, Response

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db.db_session import get_async_db
from app.models.end_user.end_user import EndUser
from app.schemas.end_user.end_user_schema import EUReqRegistrationSchema, EUResRegistrationSchema
from app.services.auth.token_service import *
from app.schemas.token_schema import TokenResponseSchema, RefreshTokenResponseSchema
from app.exceptions.customed_exceptions import (
  InternalServerError, InvalidTokenException, ResourceNotFoundException, 
  UnprocessibleContentException, InvalidRequestException,
  UnauthorizedAccessException
)
from app.services.auth.end_user_service import end_user_registration_service, end_user_auth_token_service

end_user_router = APIRouter(
  prefix="/api/enduser",
  tags=["end user API endpoints"]
)


logger = logging.getLogger(__name__)

@end_user_router.post("/registration", response_model=EUResRegistrationSchema)
async def end_user_registration_router(user: EUReqRegistrationSchema, db: AsyncSession = Depends(get_async_db)):
  try:
    new_user: EUResRegistrationSchema = await end_user_registration_service(user, db)
    
    if not new_user:
      raise UnprocessibleContentException("Value error")
    
    return new_user
  except Exception as e:
    raise InvalidRequestException("Invalid user registration")
  

@end_user_router.post("/authenticate/token", response_model=TokenResponseSchema)
async def end_user_auth_token_router(
  response: Response,
  user_cred_data: OAuth2PasswordRequestForm = Depends(),
  db: AsyncSession = Depends(get_async_db)
):
  try:
    user: EndUser = await end_user_auth_token_service(
      user_cred_data.username,
      user_cred_data.password, 
      db
    )
    
    if not user:
      raise UnauthorizedAccessException("Invalid email or password")
    
    payload={
      "sub": user.email,
      "role": str(user.role),
      "banned_until": user.banned_until.isoformat() if user.banned_until else None
    }
    
    # generate and get tokens
    access_token: str = generate_access_token(payload)
    refresh_token: str = generate_refresh_token({"sub": user.email})
    
     # attach token as http-only cookie
    response.set_cookie(
      key="refresh_token",
      value=refresh_token,
      httponly=True,       # cannot be accessed via JS
      secure=True,         # only HTTPS
      samesite="lax",      # prevents CSRF 
      max_age=7*24*60*60,  # 7 days
    )
    
    return {
      "access_token": access_token,
      "refresh_token": refresh_token,
      "token_type": "bearer"
    }
  except (UnauthorizedAccessException, ResourceNotFoundException) as e:
    logger.error("Authentication failed:", str(e))
    raise UnauthorizedAccessException("Invalid email or password")
  except Exception as e:
    logger.error("Unexpected error during authentication:", str(e))
    raise InternalServerError("An error occurred during authentication")
  

@end_user_router.post("/authenticate/refresh-token", response_model=RefreshTokenResponseSchema)
async def refresh_a_token_route(request: Request):
  """Get the refresh token from request body or cookies"""
  try:
    token = request.cookies.get("refresh_token")
  
    if not token:
      raise InvalidTokenException("No refresh token provided")
    
    return refresh_token(token)
  except Exception:
    # Handle specific refresh token errors appropriately
    raise InvalidTokenException("Invalid or expired refresh token")
  