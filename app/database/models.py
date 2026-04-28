from sqlalchemy import Integer,ARRAY
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

class user(SQLModel):
    name: str
    email: EmailStr
    password: str = Field(exclude=True)
    

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
    updated_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
            onupdate=datetime.now,
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

    delivery_partner_id:UUID=Field(
        foreign_key="deliverypartner.id",
        nullable=True
    )
    delivery_partner:"deliverypartner"=Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy":"selectin"}
    )

class Seller(user,table=True):
    __tablename__ = "seller"

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

    updated_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
            onupdate=datetime.now,
        )
    )

  

    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    
class deliverypartner(user,table=True):
    __tablename__ = "deliverypartner"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    servicable_zip_codes:list[int]=Field(
        sa_column=Column(ARRAY(Integer))
    )
    max_handling_capacity:int

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
            onupdate=datetime.now,
        )
    )


    shipments:list["Shipment"] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy":"selectin"}
    )

    