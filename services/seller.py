from passlib.context import CryptContext
from ml_fastapi.api.schemas.seller import seller_create
from sqlalchemy.ext.asyncio import AsyncSession
from ml_fastapi.database.models import Seller


pwd_context = CryptContext(schemes=["bcrypt"])


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_seller(self, seller_data: seller_create) -> Seller:
        hashed_password = pwd_context.hash(seller_data.password)
        seller = Seller(
            **seller_data.model_dump(exclude=["password"]),
            password=hashed_password
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller
