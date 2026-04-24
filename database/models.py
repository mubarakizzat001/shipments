from uuid import UUID, uuid4
from pydantic import EmailStr
from enum import Enum
from sqlmodel import SQLModel,Field,Column,Relationship
from datetime import datetime
from sqlalchemy.dialects import postgresql

class ShipmentStatus(str, Enum):
    placed = "placed"
    shipped = "shipped"
    in_transit = "in_transit"
    delivered = "delivered"
    returned = "returned"

class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    content: str
    weight: float = Field(le=25)
    destination: int
    estimated_delivery: datetime | None
    status: ShipmentStatus
    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

class Seller(SQLModel,table=True):
    __tablename__ = "seller"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    name: str

    email: EmailStr
    password: str = Field(exclude=True)

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

  

    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    
