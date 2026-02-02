from fastapi import APIRouter
from ml_fastapi.api.routers import seller,shipment



master_router=APIRouter()


master_router.include_router(seller.router)
master_router.include_router(shipment.router)

