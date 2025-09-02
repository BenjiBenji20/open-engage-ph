from pydantic import BaseModel


class TokenResponseSchema(BaseModel):
  # return 2 different token
  access_token: str
  refresh_token: str
  token_type: str
  
  class Config:
    from_attributes = True
    
    
class RefreshTokenResponseSchema(BaseModel):
  # return 2 different token
  access_token: str
  token_type: str
  
  class Config:
    from_attributes = True
  