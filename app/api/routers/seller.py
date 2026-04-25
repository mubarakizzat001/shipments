from ...database.redis import add_jti_to_blackist
from ...api.dependencies import get_access_token
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ...database.models import Seller
from ...api.schemas.seller import seller_read   
from ...api.dependencies import sellerDep,sessionDep
from ...api.schemas.seller import seller_create
from fastapi import APIRouter

from ...core.security import OAuth_schemas
from ...utils import decode_access_token




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




@router.post("/logout")
async def logout_seller(token: Annotated[dict,Depends(get_access_token)]):
    """Logs out the seller by blacklisting the JWT token."""
    await add_jti_to_blackist(token["jti"])
    return {
        "message":"logout successfully"
    }

