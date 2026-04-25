from fastapi.security import OAuth2PasswordBearer


OAuth_schemas=OAuth2PasswordBearer(tokenUrl="/seller/login")