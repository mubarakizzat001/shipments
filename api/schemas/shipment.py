
from ml_fastapi.database.models import ShipmentStatus
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4



class BaseShipment(BaseModel):
    weight: float = Field(
        le=15,
        description="weight of the shipment in kg and must be less than 15kg"
    )
    content: str = Field(
        min_length=5,
        max_length=50,
        description="content of the shipment and must be between 5 and 50 characters"
    )
    destination: int | None = None


class Shipment(BaseShipment):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    status: ShipmentStatus
    estimated_delivery: datetime | None = Field(default=None, description="estimated delivery date")


class CreateShipment(BaseShipment):
    pass


class UpdateShipment(BaseShipment):
    estimated_delivery: datetime | None = Field(default=None, description="estimated delivery date")
    status: ShipmentStatus | None = Field(default=None, description="status of the shipment")
