from typing import List, Optional
from fastapi import Depends

from app.dependencies.current_user import get_current_user
from app.exceptions.customed_exceptions import UnauthorizedAccessException
from app.models.base_user import BaseUser


def role_required(allowed_roles: List[str]):
  async def wrapper(user: Optional[BaseUser] = Depends(get_current_user)) -> None:
    if user.role not in allowed_roles:
      raise UnauthorizedAccessException("You do not have an access for this resources")
    return user
  return wrapper
