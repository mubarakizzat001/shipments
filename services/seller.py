
from ml_fastapi.config import secret_settings
from datetime import datetime,timedelta
from fastapi import HTTPException,status
from sqlalchemy import select
import bcrypt
from ml_fastapi.api.schemas.seller import seller_create
from sqlalchemy.ext.asyncio import AsyncSession
from ml_fastapi.database.models import Seller
import jwt




class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_seller(self, seller_data: seller_create) -> Seller:
        hashed_password = bcrypt.hashpw(seller_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        seller = Seller(
            **seller_data.model_dump(exclude=["password"]),
            password=hashed_password
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller

    async def login_seller(self,email,password)->str:
        ### vaildate email
        result=await self.session.execute(select(Seller).where(Seller.email==email))
        seller=result.scalar()
        if seller is None or not bcrypt.checkpw(
            password.encode('utf-8'),
            seller.password.encode('utf-8')
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="email or password is not correct",

            )
        token=jwt.encode(
            payload={
                "user" : {
                    "name":seller.name,
                    "email":seller.email,

                },
                "exp":datetime.now()+timedelta(hours=3)
            },
            algorithm=secret_settings.JWT_algorithm,
            key=secret_settings.JWT_secret
        )

        return token

