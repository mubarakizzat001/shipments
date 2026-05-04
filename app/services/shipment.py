from typing import Any
from app.api.schemas import UpdateShipment
from app.services.ShipmentEventService import ShipmentEventService
from app.services.DeliveryPartnerService import DeliveryPartnerService
from fastapi import HTTPException, status
from uuid import UUID
from app.database.models import DeliveryPartner,Seller,Shipment
from datetime import datetime,timedelta
from app.database.models import ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.shipment import CreateShipment
from app.services.Base_Service import Base_service
class shipment_service(Base_service):
    def __init__(
        self,session:AsyncSession,
        delivery_partner_service:DeliveryPartnerService,
        event_service:ShipmentEventService
        ):
        super().__init__(Shipment,session)
        self.delivery_partner_service = delivery_partner_service
        self.event_service = event_service
    async def get_shipment(self,id:UUID)->Shipment | None:
        return await self._get(id)
    

    async def post_shipment(
        self,
        shipment_data : CreateShipment,
        seller:Seller,
        )->Shipment:
        new_shipment = Shipment(
        **shipment_data.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=5),
        seller_id=seller.id
    )
        partner=await self.delivery_partner_service.assign_shipment(new_shipment)
        shipment= await self._add(new_shipment)
        event=await self.event_service.create_shipment_event(
            shipment=shipment,
            status=ShipmentStatus.placed,
            location=seller.zip_code,
            description=f"assigned to {partner.name}"
            )
        shipment.timeline.append(event)
        return shipment


    async def patch_shipment(self,id:UUID,shipment_update:UpdateShipment,partner:DeliveryPartner)->Shipment:
        shipment_obj=await self._get(id)
        if shipment_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if partner.id != shipment_obj.delivery_partner_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized")
        shipment=shipment_update.model_dump(exclude_none=True)
        if shipment_update.estimated_delivery:
            shipment_obj.estimated_delivery = shipment_update.estimated_delivery
        
       
        event=await self.event_service.create_shipment_event(
          shipment=shipment_obj,
          **shipment
        )
        shipment_obj.timeline.append(event)
        return await self._patch(shipment_obj)



    async def cancel_shipment(self,id:UUID,seller:Seller)->Shipment:
        shipment_obj=await self._get(id)
        if shipment_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if seller.id != shipment_obj.seller_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized")
        shipment_obj.status=ShipmentStatus.cancelled
        event=await self.event_service.create_shipment_event(
            shipment=shipment_obj,
            status=ShipmentStatus.cancelled,
            location=seller.zip_code,
            description="cancelled by seller"
            )
        shipment_obj.timeline.append(event)
        return await self._patch(shipment_obj)

    async def delete_shipment(self,id:UUID)->None:
        return await self._delete(await self._get(id))