from sqlalchemy import select
from typing import Type, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base_user import BaseUser
from app.models.photo.user_photo import UserPhoto
from app.models.end_user.end_user import EndUser
from app.models.admin.admin import Admin
from app.models.regulator.regulator import Regulator
from app.models.moderator.moderator import Moderator

# Define a union of all possible user types
UserModel = Union[EndUser, Admin, Moderator, Regulator]

async def get_user_by_email(
  db: AsyncSession,
  model: Type[BaseUser],
  email: str
) -> Optional[BaseUser]:
  """Get user by email address"""
  result = await db.execute(
      select(model).where(model.email.ilike(email))
  )
  return result.scalar_one_or_none()


async def upload_photo(
  db: AsyncSession,
  user: UserModel,  
  filename: str,
  file_url: str = None,
  file_size: int = None,
  mime_type: str = None,
  is_profile_photo: bool = False,
  description: str = None
) -> UserPhoto:
  """Create and save a UserPhoto linked to a user instance"""
  photo = UserPhoto(
    filename=filename,
    file_url=file_url,
    file_size=file_size,
    mime_type=mime_type,
    is_profile_photo=is_profile_photo,
    description=description
  )
  
  # Attach to the correct relationship based on user type
  if isinstance(user, EndUser):
    photo.end_user = user  
  elif isinstance(user, Admin):
    photo.admin = user 
  elif isinstance(user, Moderator):
    photo.moderator = user 
  elif isinstance(user, Regulator):
    photo.regulator = user 
  else:
    raise ValueError(f"Unsupported user model: {type(user)}")
  
  # Save to database
  db.add(photo)
  await db.commit()
  await db.refresh(photo)
  
  return photo
