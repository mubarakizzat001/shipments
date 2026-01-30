from enum import Enum
from pydantic import BaseModel, Field


class ShipmentStatus(str, Enum):
    placed = "placed"
    shipped = "shipped"
    in_transit = "in_transit"
    delivered = "delivered"
    returned = "returned"


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
    destination: int


class read_shipment(baseShipment):
    status:ShipmentStatus

class create_shipment(baseShipment):
    pass

class update_shipment(baseShipment):
    content:str|None=Field(default=None,description="content of the shipment and must be between 5 and 50 characters")
    weight:float|None=Field(default=None,description="weight of the shipment in kg and must be less than 15kg")
    destination:int|None=Field(default=None,description="destination of the shipment")
    status:ShipmentStatus|None=Field(default=None,description="status of the shipment")    
