### shipment management api
from datetime import datetime, timedelta
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from ml_fastapi.database.session import create_db_table, sessionDep
from .schemas import ReadShipment, CreateShipment, UpdateShipment
from ml_fastapi.database.models import Shipment, ShipmentStatus


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_table()
    yield


### create fastapi app
app = FastAPI(lifespan=lifespan_handler)


### read shipment by id 
@app.get("/shipments/{shipment_id}", response_model=ReadShipment)
def get_shipment(shipment_id: int, session: sessionDep) -> Any:
    shipment_obj = session.get(Shipment, shipment_id)
    if shipment_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return shipment_obj


### create new shipment     
@app.post("/shipments", response_model=None)
def create(shipment_data: CreateShipment, session: sessionDep) -> dict[str, Any]:
    new_shipment = Shipment(
        **shipment_data.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=5)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id": new_shipment.id}


### update shipment by id
@app.patch("/shipments/{shipment_id}", response_model=UpdateShipment)
def update(shipment_id: int, shipment_update: UpdateShipment, session: sessionDep) -> Any:
    updated_data = shipment_update.model_dump(exclude_none=True)
    if not updated_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no update data provided")
    shipment_obj = session.get(Shipment, shipment_id)
    if shipment_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    shipment_obj.sqlmodel_update(updated_data)
    session.add(shipment_obj)
    session.commit()
    session.refresh(shipment_obj)
    return shipment_obj


### delete shipment by id
@app.delete("/shipments/{shipment_id}")
def delete(shipment_id: int, session: sessionDep) -> dict[str, Any]:
    ### remove shipment from dataset
    shipment_obj = session.get(Shipment, shipment_id)
    if shipment_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(shipment_obj)
    session.commit()

    return {"message": f"shipment {shipment_id} deleted"}



### scalar endpoint
@app.get("/scalar")
def scalar_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar FastAPI Example"

    )