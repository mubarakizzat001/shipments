
from pydantic import BaseModel, Field
from .database.models import ShipmentStatus
from datetime import datetime




class baseShipment(BaseModel):
    weight: float = Field(
        le=15,
        description="weight of the shipment in kg and must be less than 15kg"
    )
    content: str = Field(
        min_length=5,
        max_length=50,
        description="content of the shipment and must be between 5 and 50 characters"
    )
    destination: str | None = None


class read_shipment(baseShipment):
    status:ShipmentStatus
    estimated_delivery:datetime|None=Field(default=None,description="estimated delivery date")

class create_shipment(baseShipment):
    pass

class update_shipment(BaseModel):
    estimated_delivery:datetime|None=Field(default=None,description="estimated delivery date")
    status:ShipmentStatus|None=Field(default=None,description="status of the shipment")    
