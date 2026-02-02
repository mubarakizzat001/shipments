
from ml_fastapi.database.models import ShipmentStatus
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import SQLModel, Field




class BaseShipment(SQLModel):
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


class Shipment(BaseShipment, table=True):
    __tablename__="shipment"
    id: int = Field(primary_key=True)
    status: ShipmentStatus
    estimated_delivery: datetime | None = Field(default=None, description="estimated delivery date")


class CreateShipment(BaseShipment):
    pass


class UpdateShipment(BaseShipment):
    estimated_delivery: datetime | None = Field(default=None, description="estimated delivery date")
    status: ShipmentStatus | None = Field(default=None, description="status of the shipment")
