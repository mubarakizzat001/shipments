
from fastapi import HTTPException,status
from sqlalchemy import select
import bcrypt
from ml_fastapi.api.schemas.seller import seller_create
from sqlalchemy.ext.asyncio import AsyncSession
from ml_fastapi.database.models import Seller
from ml_fastapi.utils import generate_access_token




class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_seller(self, seller_data: seller_create) -> Seller:
        hashed_password = bcrypt.hashpw(seller_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        seller = Seller(
            **seller_data.model_dump(exclude={"password"}),
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
        token= generate_access_token(
            data={
                "name":seller.name,
                "email":seller.email
            },
        )

        return token

