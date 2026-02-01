from enum import Enum
from sqlmodel import SQLModel
from datetime import datetime

class ShipmentStatus(str, Enum):
    placed = "placed"
    shipped = "shipped"
    in_transit = "in_transit"
    delivered = "delivered"
    returned = "returned"

class shipment(SQLModel,table=True):
    __tablename__="shipment"
    id : int =Field(primary_key=True)
    weight:float=Field(le=15)
    content:str
    destination:str
    status:ShipmentStatus
    estimated_delivery:datetime
