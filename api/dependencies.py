from ml_fastapi.database.models import Seller
from fastapi import HTTPException,status
from ml_fastapi.utils import decode_access_token
from ml_fastapi.core.security import OAuth_schemas
from ml_fastapi.services.seller import SellerService
from ml_fastapi.services.shipment import shipment_service
from ml_fastapi.database.session import get_session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


sessionDep= Annotated[AsyncSession,Depends(get_session)]

def get_access_token(token:Annotated[str,Depends(OAuth_schemas)])->dict:
    data = decode_access_token(token)  
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expired login credentials",
        )
    return data

async def get_current_seller(token_data :Annotated[dict,Depends(get_access_token)],
                          session:sessionDep,
):
    return await session.get(Seller, token_data["user"]["id"])


def get_shipment_service(session:sessionDep):
    return shipment_service(session)

def get_seller_service(session:sessionDep):
    return SellerService(session)


activesellerDep=Annotated[Seller,Depends(get_current_seller)]
serviceDep=Annotated[shipment_service,Depends(get_shipment_service)]

sellerDep=Annotated[SellerService,Depends(get_seller_service)]