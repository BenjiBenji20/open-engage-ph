from fastapi.security import OAuth2PasswordBearer


end_user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/enduser/authenticate/token")