from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ml_fastapi.api.schemas.seller import seller_read   
from ml_fastapi.api.dependencies import sellerDep
from ml_fastapi.api.schemas.seller import seller_create
from fastapi import APIRouter

from ml_fastapi.core.security import OAuth_schemas
from ml_fastapi.utils import decode_access_token




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



@router.get("/dashboard")
def dashboard(token: Annotated[str,Depends(OAuth_schemas)]):
    data = decode_access_token(token)  # noqa: F841
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid login credentials",
        )
    
    return {
        "message":"successful login"
    }

