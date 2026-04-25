from app.database.redis import is_token_blacklisted
from app.database.models import Seller
from fastapi import HTTPException,status
from app.utils import decode_access_token
from app.core.security import OAuth_schemas
from app.services.seller import SellerService
from app.services.shipment import shipment_service
from app.database.session import get_session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


sessionDep= Annotated[AsyncSession,Depends(get_session)]

async def get_access_token(token:Annotated[str,Depends(OAuth_schemas)])->dict:
    data = decode_access_token(token)  
    if data is None or await is_token_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expired login credentials",
        )
    return data

async def get_current_seller(token_data :Annotated[dict,Depends(get_access_token)],
                          session:sessionDep,
):
    return await session.get(Seller, UUID(token_data["user"]["id"]))


def get_shipment_service(session:sessionDep):
    return shipment_service(session)

def get_seller_service(session:sessionDep):
    return SellerService(session)


activesellerDep=Annotated[Seller,Depends(get_current_seller)]
serviceDep=Annotated[shipment_service,Depends(get_shipment_service)]

sellerDep=Annotated[SellerService,Depends(get_seller_service)]