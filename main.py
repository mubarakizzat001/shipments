
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from .schemas import read_shipment,create_shipment,update_shipment


app = FastAPI()

### Shipments datastore as dict
shipments = {
    12701: {"weight": 0.6, "content": "rubber ducks", "status": "placed"},
    12702: {"weight": 2.3, "content": "magic wands", "status": "shipped"},
    12703: {"weight": 1.1, "content": "unicorn horns", "status": "delivered"},
    12704: {"weight": 3.5, "content": "dragon eggs", "status": "in transit"},
    12705: {"weight": 0.9, "content": "wizard hats", "status": "returned"},
}
### read shipment by id 
@app.get("/shipments/{shipment_id}",response_model=read_shipment)
def get_shipment(shipment_id: int) -> dict[str, Any]:
    if shipment_id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return shipments[shipment_id]


### create new shipment     
@app.post("/shipments",response_model=create_shipment)
def create_shipment(shipment:create_shipment) -> dict[str, Any]:
    if shipment.weight > 15:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Shipment too heavy")
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = shipment.model_dump()
    return {"id": new_id}



### update shipment by id
@app.patch("/shipments",response_model=update_shipment)
def update_shipment(id: int, shipment: update_shipment) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    shipments[id].update(shipment)
    return shipments[id]

### delete shipment by id
@app.delete("/shipments")
def delete_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    shipments.pop(id)
    return {"message": f"shipment {id} deleted"}



### scalar endpoint
@app.get("/scalar")
def scalar_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar FastAPI Example"

    )