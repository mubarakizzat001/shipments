from typing import Annotated
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ml_fastapi.api.schemas.seller import seller_read   
from ml_fastapi.api.dependencies import sellerDep
from ml_fastapi.api.schemas.seller import seller_create
from fastapi import APIRouter




router=APIRouter(prefix="/seller",tags=["seller"])


### register seller
@router.post("/signup",response_model=seller_read)
async def register_seller(seller:seller_create,service:sellerDep):
    
    return await service.register_seller(seller)
 

### login seller
@router.post("/login")
async def login_seller(
    request_form:Annotated[OAuth2PasswordRequestForm,Depends()],
    service:sellerDep,
):
    
    token= await service.login_seller(request_form.username,request_form.password)
    
    return {
        "access_token":token,
        "type":"jwt"
    }



