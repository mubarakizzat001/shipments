from app.services.ShipmentEventService import ShipmentEventService
from app.services.DeliveryPartnerService import DeliveryPartnerService
from app.database.redis import is_token_blacklisted
from app.database.models import Seller,DeliveryPartner
from fastapi import HTTPException,status
from app.utils import decode_access_token
from app.core.security import OAuth_schemas_seller,OAuth_schemas_deliverypartner
from app.services.seller import SellerService
from app.services.shipment import shipment_service
from app.database.session import get_session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


sessionDep= Annotated[AsyncSession,Depends(get_session)]

async def _get_access_token(token:str)->dict:
    data = decode_access_token(token)  
    if data is None or await is_token_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expired login credentials",
        )
    return data


async def get_access_token_seller(
    token:Annotated[str,Depends(OAuth_schemas_seller)],
):
    return await _get_access_token(token)
async def get_access_token_deliverypartner(
    token:Annotated[str,Depends(OAuth_schemas_deliverypartner)],
):
    return await _get_access_token(token)


async def get_current_seller(token_data :Annotated[dict,Depends(get_access_token_seller)],
                          session:sessionDep,
):
    seller= await session.get(Seller, UUID(token_data["user"]["id"]))
    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="seller not found",
        )
    return seller

async def get_current_deliverypartner(token_data :Annotated[dict,Depends(get_access_token_deliverypartner)],
                          session:sessionDep,
):
    delivery_partner= await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))
    if delivery_partner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="deliverypartner not found",
        )
    return delivery_partner

def get_shipment_service(session:sessionDep):
    return shipment_service(session,DeliveryPartnerService(session),ShipmentEventService(session))

def get_seller_service(session:sessionDep):
    return SellerService(session)
def get_deliverypartner_service(session:sessionDep):
    return DeliveryPartnerService(session)

activesellerDep=Annotated[Seller,Depends(get_current_seller)]
active_deliverypartnerDep=Annotated[DeliveryPartner,Depends(get_current_deliverypartner)]
serviceDep=Annotated[shipment_service,Depends(get_shipment_service)]
sellerDep=Annotated[SellerService,Depends(get_seller_service)]
deliverypartnerDep=Annotated[DeliveryPartnerService,Depends(get_deliverypartner_service)]
