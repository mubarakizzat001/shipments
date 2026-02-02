from ml_fastapi.api.dependencies import serviceDep
from fastapi import APIRouter
from ml_fastapi.api.schemas import CreateShipment, UpdateShipment,Shipment
from typing import Any
from fastapi import HTTPException, status



router=APIRouter(prefix="/api",tags=["shipments"])


### read shipment by id 
@router.get("/", response_model=Shipment)
async def get_shipment(shipment_id: int, service: serviceDep) -> Any:
    shipment_obj = await service.get_shipment(shipment_id)
    if shipment_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return shipment_obj


### create new shipment     
@router.post("/")
async def create(shipment_data: CreateShipment, service: serviceDep) -> Shipment:
    return await service.post_shipment(shipment_data)
   

### update shipment by id
@router.patch("/", response_model=UpdateShipment)
async def update(shipment_id: int, shipment_update: UpdateShipment, service: serviceDep) -> Any:
    updated_data = shipment_update.model_dump(exclude_none=True)
    if not updated_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no update data provided")
    shipment_obj= await service.patch_shipment(shipment_id,shipment_update)
    return shipment_obj


### delete shipment by id
@router.delete("/")
async def delete(shipment_id: int, service: serviceDep) -> dict[str, Any]:
    ### remove shipment from dataset
    await service.delete_shipment(shipment_id)

    return {"message": f"shipment {shipment_id} deleted"}

