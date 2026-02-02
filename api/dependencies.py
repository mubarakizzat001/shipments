from ml_fastapi.services.shipment import shipment_service
from ml_fastapi.database.session import get_session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


sessionDep= Annotated[AsyncSession,Depends(get_session)]


def get_shipment_service(session:sessionDep):
    return shipment_service(session)


serviceDep=Annotated[shipment_service,Depends(get_shipment_service)]