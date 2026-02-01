### shipment management api
from datetime import datetime, timedelta
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from shipment_fastapi.database.session import create_db_table,sessionDep
from .schemas import read_shipment,create_shipment,update_shipment
from shipment_fastapi.database.models import shipment


@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    create_db_table()
    yield


### create fastapi app
app = FastAPI(lifespan=lifespan_handler)


### read shipment by id 
@app.get("/shipments/{shipment_id}",response_model=read_shipment)
def get_shipment(shipment_id: int,session:sessionDep) -> dict[str, Any]:
    shipment=session.get(shipment,shipment_id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return shipment


### create new shipment     
@app.post("/shipments", response_model=dict)
def create_shipment(shipment:create_shipment,session:sessionDep) -> dict[str, Any]:
    new_shipment=shipment(
        **shipment.model_dump(),
        status=shipment.status.placed,
        estimated_delivery=datetime.now()+timedelta(days=5)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id": new_shipment.id}


### update shipment by id
@app.patch("/shipments",response_model=update_shipment)
def update_shipment(id: int, shipment_update: update_shipment,session:sessionDep) -> dict[str, Any]:
    updated=shipment_update.model_dump(exclude_none==True)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="no update data provided")
    shipment=session.get(shipment,id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    shipment.sqlmodel_update(updated)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment

### delete shipment by id
@app.delete("/shipments")
def delete_shipment(id: int,session:sessionDep) -> dict[str, Any]:
    ### remove shipment from dataset
    session.delete(session.get(shipment,id))
    session.commit()

    return {"message": f"shipment {id} deleted"}



### scalar endpoint
@app.get("/scalar")
def scalar_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar FastAPI Example"

    )