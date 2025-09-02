
from typing import Literal
from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  APP_NAME: str
  DEBUG: bool = True
  ENV: Literal["dev", "prod", "test"] = "dev"
  
  # db settings
  POSTGRES_USER: str
  POSTGRES_PASSWORD: SecretStr
  POSTGRES_HOST: str
  POSTGRES_PORT: str
  POSTGRES_DATABASE: str
  # mongodb
  MONGO_DB_URI: str
  MONGO_DB_NAME: str
  
  #auth security
  MAX_FAILED_ATTEMPTS: int 
  BAN_DURATION_MINUTES: int
  
  # JWT settings
  JWT_SECRET_KEY: str
  JWT_ALGORITHM: str
  ACCESS_TOKEN_EXPIRE_MINUTES: int
  
  class Config:
    env_file = ".env"
    extra = "ignore"
    
  @property
  def DATABASE_URL(self) -> PostgresDsn:
    return (
      f"postgresql+asyncpg://{self.POSTGRES_USER}:"
      f"{self.POSTGRES_PASSWORD.get_secret_value()}"
      f"@{self.POSTGRES_HOST}:"
      f"{self.POSTGRES_PORT}/"
      f"{self.POSTGRES_DATABASE}"
    )
    
    
settings = Settings()
    