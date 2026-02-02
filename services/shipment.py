


from datetime import datetime,timedelta
from ml_fastapi.database.models import ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession
from ml_fastapi.api.schemas.shipment import CreateShipment,Shipment

class shipment_service:
    def __init__(self,session:AsyncSession):
        self.session=session


    async def get_shipment(self,shipment_id:int)->Shipment:


        return await self.session.get(Shipment,shipment_id)
    

    async def post_shipment(self,shipment_data : CreateShipment)->Shipment:
        new_shipment = Shipment(
        **shipment_data.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=5)
    )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment


    async def patch_shipment(self,shipment_id:int,shipment_update:dict)->Shipment:
        shipment_obj =await self.get_shipment(shipment_id)
        shipment_obj.sqlmodel_update(shipment_update)
        self.session.add(shipment_obj)
        await self.session.commit()
        await self.session.refresh(shipment_obj)
        return shipment_obj


    async def delete_shipment(self,shipment_id:int)->None:
        shipment_obj = await self.get_shipment(shipment_id)
        await self.session.delete(shipment_obj)
        await self.session.commit()