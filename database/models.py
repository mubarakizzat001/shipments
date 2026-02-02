from enum import Enum
from sqlmodel import SQLModel,Field
from datetime import datetime

class ShipmentStatus(str, Enum):
    placed = "placed"
    shipped = "shipped"
    in_transit = "in_transit"
    delivered = "delivered"
    returned = "returned"

#class Shipment(SQLModel, table=True):
    # __tablename__ = "shipment"
    # id: int = Field(primary_key=True)
    # weight: float = Field(le=15)
    # content: str
    # destination: str
    # status: ShipmentStatus
    # estimated_delivery: datetime
