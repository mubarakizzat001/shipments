from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference


app = FastAPI()

### Shipments datastore as dict
shipments = {
    12701: {"weight": 0.6, "content": "rubber ducks", "status": "placed"},
    12702: {"weight": 2.3, "content": "magic wands", "status": "shipped"},
    12703: {"weight": 1.1, "content": "unicorn horns", "status": "delivered"},
    12704: {"weight": 3.5, "content": "dragon eggs", "status": "in transit"},
    12705: {"weight": 0.9, "content": "wizard hats", "status": "returned"},
}

@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id:int)->dict[str,Any]:
    if shipment_id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return shipments[shipment_id]

@app.post("/shipments")
def create_shipment(shipment:dict[str,Any])->dict[str,Any]:
    new_id = max(shipments.keys())+1
    shipments[new_id] = shipment
    return {"id":new_id}


    


@app.get("/scalar")
def scalar_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar FastAPI Example"

    )