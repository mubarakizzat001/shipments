from enum import Enum
from pydantic import BaseModel, Field


class ShipmentStatus(str, Enum):
    placed = "placed"
    shipped = "shipped"
    in_transit = "in_transit"
    delivered = "delivered"
    returned = "returned"


class Shipment(BaseModel):
    weight: float = Field(
        le=15,
        description="weight of the shipment in kg and must be less than 15kg"
    )
    content: str = Field(
        min_length=5,
        max_length=50,
        description="content of the shipment and must be between 5 and 50 characters"
    )
    status: ShipmentStatus