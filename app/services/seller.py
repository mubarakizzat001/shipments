
from fastapi import HTTPException,status
import bcrypt
from app.api.schemas.seller import seller_create
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Seller
from app.utils import generate_access_token


from app.services.Base_User import Base_User

class SellerService(Base_User):
    def __init__(self, session: AsyncSession):
        super().__init__(Seller,session)

    async def register_seller(self, seller_data: seller_create) -> Seller:
        return await self._create_user(seller_data)

    async def login_seller(self,email,password)->str:
        return await self._login(email,password)


    