from sqlalchemy import select
from typing import TypeVar, Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base_user import BaseUser

T = TypeVar("T", bound=BaseUser)  # subclass of BaseUser abstract model

async def get_user_by_email(
  model: Type[T],
  email: str,
  db: AsyncSession
) -> Optional[T]:
  result = await db.execute(
    select(model).where(model.email.ilike(email))
  )
  
  return result.scalar_one_or_none()
