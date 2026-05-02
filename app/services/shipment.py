from app.services.DeliveryPartnerService import DeliveryPartnerService
from uuid import UUID
from app.database.models import Seller,Shipment
from datetime import datetime,timedelta
from app.database.models import ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.shipment import CreateShipment
from app.services.Base_Service import Base_service
class shipment_service(Base_service):
    def __init__(self,session:AsyncSession,delivery_partner_service:DeliveryPartnerService):
        super().__init__(Shipment,session)
        self.delivery_partner_service = delivery_partner_service

    async def get_shipment(self,id:UUID)->Shipment | None:
        return await self._get(id)
    

    async def post_shipment(self,shipment_data : CreateShipment,seller:Seller)->Shipment:
        new_shipment = Shipment(
        **shipment_data.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=5),
        seller_id=seller.id
    )
        await self.delivery_partner_service.assign_shipment(new_shipment)
        return await self._add(new_shipment)


    async def patch_shipment(self,id:UUID,shipment_update:dict)->Shipment:
        shipment_obj =await self.get_shipment(id)
        shipment_obj.sqlmodel_update(shipment_update)
        shipment = await self._patch(shipment_obj)
        return shipment


    async def delete_shipment(self,id:UUID)->None:
        await self._delete(await self._get(id))