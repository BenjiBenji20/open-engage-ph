from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_session import get_async_db
from app.exceptions.customed_exceptions import (
  InternalServerError, InvalidTokenException, 
)
from app.schemas.token_schema import RefreshTokenResponseSchema, TokenResponseSchema
from app.models.base_user import BaseUser
from app.services.auth.auth_service import *

auth_router = APIRouter(
  prefix="/api/user",
  tags=["General user authentication router"]
)
  
  
@auth_router.post("/authenticate/token", response_model=TokenResponseSchema)
async def end_user_auth_token_router(
  response: Response,
  user_cred_data: OAuth2PasswordRequestForm = Depends(),
  db: AsyncSession = Depends(get_async_db)
):
  try:
    user: BaseUser = await auth_token_service(
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
    logger.error("Authentication failed: %s", str(e))
    raise UnauthorizedAccessException("Invalid email or password")
  except Exception as e:
    logger.error("Unexpected error during authentication: %s", str(e))
    raise InternalServerError("An error occurred during authentication")
  

@auth_router.post("/authenticate/refresh-token", response_model=RefreshTokenResponseSchema)
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
  