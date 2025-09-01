from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.db_session import engine
from app.db.base import Base
# Models
from app.models.base_user import BaseUser
from app.models.end_user.end_user import EndUser
from app.models.admin.admin import Admin
from app.models.moderator.moderator import Moderator
from app.models.regulator.regulator import Regulator
from app.models.oauth.oauth import UserOAuth
from app.models.photo.user_photo import UserPhoto
from app.models.ordinance.ordinance import Ordinance


@asynccontextmanager
async def life_span(app: FastAPI):
  try:
    async with engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all)
      print("table are created successfully!")
      
    yield

  finally:
    await engine.dispose()
    print("Application shutdown...")
    
    
app = FastAPI(lifespan=life_span)
