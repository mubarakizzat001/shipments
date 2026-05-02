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

class User(SQLModel):
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
        foreign_key="DeliveryPartner.id",
        nullable=True
    )
    delivery_partner:"DeliveryPartner"=Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy":"selectin"}
    )

class Seller(User,table=True):
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

    
class DeliveryPartner(User,table=True):
    __tablename__ = "DeliveryPartner"

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


    @property
    def active_shipments(self):
        return [
            shipment for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered and shipment.status != ShipmentStatus.returned
        ]

    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)
