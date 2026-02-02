from ml_fastapi.api.schemas.seller import seller_read   
from ml_fastapi.api.dependencies import sellerDep
from ml_fastapi.api.schemas.seller import seller_create
from fastapi import APIRouter




router=APIRouter(prefix="/seller",tags=["seller"])



@router.post("/signup",response_model=seller_read)
async def register_seller(seller:seller_create,serivce:sellerDep):
    
    return await service.register_seller(seller)
