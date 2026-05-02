from fastapi import HTTPException,status
from app.database.models import Shipment
from typing import Sequence
from sqlmodel import select,any_
from app.database.models import DeliveryPartner
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.Base_User import Base_User
from app.api.schemas.delivery_partner import DeliveryPartner_Create,DeliveryPartner_Read,DeliveryPartner_Update

class DeliveryPartnerService(Base_User):
    def __init__(self, session: AsyncSession):
        super().__init__(DeliveryPartner,session)

    async def register(self,data:DeliveryPartner_Create):
        return await self._create_user(data)
    
    async def update(self,data:DeliveryPartner_Update):
        return await self._patch(data)
    
    async def login(self,email:str,password:str)->str:
        return await self._login(email,password)
    
    async def get_partner_by_zipcode(self,zipcode:int)->Sequence[DeliveryPartner]:
        return (await self.session.scalars(
            select(DeliveryPartner).where(
                zipcode== any_(DeliveryPartner.servicable_zip_codes)
            )
        )).all()

    
    async def assign_shipment(self,shipment:Shipment):
        eligible_partner= await self.get_partner_by_zipcode(shipment.destination)

        for partner in eligible_partner:
            if partner.current_handling_capacity>0:
                partner.shipments.append(shipment)
                return partner

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No eligible partner found"
        )
           
    
    