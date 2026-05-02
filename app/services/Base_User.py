

from app.utils import generate_access_token
from fastapi import HTTPException,status
import bcrypt
from pydantic import EmailStr
from sqlmodel import select
from app.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.Base_Service import Base_service
class Base_User(Base_service):


    def __init__(self,model:User,session:AsyncSession):
        self.session=session
        self.model=model


    async def _create_user(self,data:dict):
        
        password_hash=bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user=self.model(
            **data.model_dump(exclude={"password"}),
           password=password_hash,
        )
        return await self._add(user)


    async def _get_user_by_email(self,email:EmailStr)->User |None:
        return await self.session.scalar(
            select(self.model).where(self.model.email==email)
        )

    async def _login(self,email,password)->str:
        ### vaildate email
        user=await self._get_user_by_email(email)
    
        if user is None or not bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="email or password is not correct",

            )
        return  generate_access_token(
            data={
                "name":user.name,
                "id":str(user.id)
            },
        )

   



    