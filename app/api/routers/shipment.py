from app.api.dependencies import active_deliverypartnerDep
from app.database.models import DeliveryPartner
from app.api.dependencies import deliverypartnerDep,activesellerDep,serviceDep
from fastapi import APIRouter
from ..schemas import CreateShipment, UpdateShipment,Shipment
from typing import Any
from fastapi import HTTPException, status
from uuid import UUID



router=APIRouter(prefix="/api",tags=["shipments"])


### read shipment by id 
@router.get("/", response_model=Shipment)
async def get_shipment(seller:activesellerDep,shipment_id: UUID, service: serviceDep) -> Any:
    shipment_obj = await service.get_shipment(shipment_id)
    if shipment_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return shipment_obj


### create new shipment     
@router.post("/")
async def create(   shipment_data: CreateShipment,
    seller: activesellerDep,
    service: serviceDep) -> Shipment:
    return await service.post_shipment(shipment_data,seller)
   

### update shipment by id
@router.patch("/", response_model=Shipment)
async def update(
    id: UUID,
    shipment_update: UpdateShipment,
    service: serviceDep,
    partner:active_deliverypartnerDep
      ) -> Any:
  
    return await service.patch_shipment(
        id,
        shipment_update,
        partner
    )



### cancel shipment by id
@router.get("/cancel",response_model=Shipment)
async def cancel_shipment(
    id: UUID, 
    service: serviceDep,
    seller:activesellerDep
) -> Shipment:
    ### cancel shipment by id
    return await service.cancel_shipment(id,seller)

