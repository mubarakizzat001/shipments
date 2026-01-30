### shipment management api
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from .schemas import read_shipment,create_shipment,update_shipment
from .database import shipments,save_shipments
### create fastapi app
app = FastAPI()


### read shipment by id 
@app.get("/shipments/{shipment_id}",response_model=read_shipment)
def get_shipment(shipment_id: int) -> dict[str, Any]:
    if shipment_id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return shipments[shipment_id]


### create new shipment     
@app.post("/shipments", response_model=dict)
def create_shipment(shipment:create_shipment) -> dict[str, Any]:
    if shipment.weight > 15:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Shipment too heavy")
    new_id = (max(shipments.keys()) if shipments else 0) + 1
    shipments[new_id] = {
        "id": new_id,
        **shipment.model_dump(),
        "status": "placed"
        }
    save_shipments()
    return {"id": new_id}



### update shipment by id
@app.patch("/shipments",response_model=update_shipment)
def update_shipment(id: int, shipment: update_shipment) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    shipments[id].update(shipment.model_dump(exclude_unset=True))
    save_shipments()
    return shipments[id]

### delete shipment by id
@app.delete("/shipments")
def delete_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    shipments.pop(id)
    save_shipments()
    return {"message": f"shipment {id} deleted"}



### scalar endpoint
@app.get("/scalar")
def scalar_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar FastAPI Example"

    )