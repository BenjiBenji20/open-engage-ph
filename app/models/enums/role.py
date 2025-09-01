from enum import Enum

class ModelRole(str, Enum):
  END_USER = "end_user"
  ADMIN = "admin"
  MODERATOR = "moderator"
  REGULATOR = "regulator"
  
  COMMENT = "comment"
  