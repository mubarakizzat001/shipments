

from uuid import uuid4
from fastapi import HTTPException,status
from datetime import timezone
from datetime import datetime, timedelta
import token
import jwt
from app.api.schemas import seller
from app.config import secret_settings

def generate_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(hours=4)

)->str:
    return jwt.encode(
            payload={
                "user" : {
                    **data
                },
                "exp":datetime.now(timezone.utc)+expires_delta,
                "jti":str(uuid4())
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

   except jwt.ExpiredSignatureError:
      raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token expired",
        )
   except jwt.PyJWTError:
      return None 