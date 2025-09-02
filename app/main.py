from contextlib import asynccontextmanager
from fastapi import FastAPI

from motor.motor_asyncio import AsyncIOMotorClient

from app.db.db_session import engine
from app.configs.settings import settings
from app.db.base import Base
import app.state.mongodb_client_state as state

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
      print("RDBMS table are created successfully!")
      
    # mongodb client and db startup
    client = AsyncIOMotorClient(settings.MONGO_DB_URI)
    # mutating state variables for cross module access
    state.mongo_client = client
    state.mongo_db = client[settings.MONGO_DB_NAME]
    print("Successfully connected to NoSQL DB!")
      
    yield

  finally:
    await engine.dispose()
    print("RDBMS engine disposed...")
    
    # mongodb client shutdown
    client.close()
    print("NoSQL client connection closed...")
    print("Application shutdown...")
    
    
app = FastAPI(lifespan=life_span)
