from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db.db_session import get_async_db
from app.schemas.admin.admin_schema import AdminRequestSchema, AdminResponseSchema
from app.exceptions.customed_exceptions import UnprocessibleContentException, InvalidRequestException
from app.services.admin.admin_service import admin_registration_service

admin_router = APIRouter(
  prefix="/api/admin",
  tags=["admin API endpoints"]
)


logger = logging.getLogger(__name__)

@admin_router.post("/registration", response_model=AdminResponseSchema)
async def admin_registration_router(user: AdminRequestSchema, db: AsyncSession = Depends(get_async_db)):
  try:
    new_user: AdminResponseSchema = await admin_registration_service(user, db)
    
    if not new_user:
      raise UnprocessibleContentException("Value error")
    
    return new_user
  except Exception as e:
    raise InvalidRequestException("Invalid user registration")
