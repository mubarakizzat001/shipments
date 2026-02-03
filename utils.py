

from datetime import datetime, timedelta
import token
import jwt
from ml_fastapi.api.schemas import seller
from ml_fastapi.config import secret_settings

def generate_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(hours=3)

)->str:
    return jwt.encode(
            payload={
                "user" : {
                    **data
                },
                "exp":datetime.now()+expires_delta
            },
            algorithm=secret_settings.JWT_algorithm,
            key=secret_settings.JWT_secret
        )
    



def decode_access_token(token:str)->dict|None:


   try:
    return jwt.decode(
        jwt=token,
        key=secret_settings.JWT_secret,
        algorithms=[secret_settings.JWT_algorithm]
    )
   except jwt.PyJWTError:
      return None