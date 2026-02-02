from pydantic import EmailStr
from enum import Enum
from sqlmodel import SQLModel,Field
from datetime import datetime

class ShipmentStatus(str, Enum):
    placed = "placed"
    shipped = "shipped"
    in_transit = "in_transit"
    delivered = "delivered"
    returned = "returned"



class Seller(SQLModel,table=True):
    id: int = Field(default=None,primary_key=True)
    name: str
    email: EmailStr
    password: str
    
