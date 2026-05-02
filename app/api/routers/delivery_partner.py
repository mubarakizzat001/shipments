from app.api.dependencies import active_deliverypartnerDep
from ...database.redis import add_jti_to_blackist
from ...api.dependencies import get_access_token_deliverypartner
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ...database.models import DeliveryPartner
from ...api.dependencies import deliverypartnerDep,sessionDep
from ...api.schemas.delivery_partner import DeliveryPartner_Create,DeliveryPartner_Update,DeliveryPartner_Read
from fastapi import APIRouter




router=APIRouter(prefix="/deliverypartner",tags=["deliverypartner"])


### register deliverypartner
@router.post("/signup",response_model=DeliveryPartner_Read)
async def register_deliverypartner(deliverypartner:DeliveryPartner_Create,service:deliverypartnerDep):
    
    return await service.register(deliverypartner)
 

### login deliverypartner
@router.post("/login")
async def login_deliverypartner(
    request_form:Annotated[OAuth2PasswordRequestForm,Depends()],
    service:deliverypartnerDep,
):
    
    token= await service.login(request_form.username,request_form.password)
    
    return {
        "access_token":token,
        "type":"jwt"
    }


@router.post("/update")
async def update_deliverypartner(
    deliverypartner:DeliveryPartner_Update,
    partner:active_deliverypartnerDep,
    service:deliverypartnerDep
):

    update=deliverypartner.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided"
        )
        
    return await service.update(
        partner.sqlmodel_update(
            update
        )
    )

@router.get("/logout")
async def logout_deliverypartner(token: Annotated[dict,Depends(get_access_token_deliverypartner)]):
    """Logs out the deliverypartner by blacklisting the JWT token."""
    await add_jti_to_blackist(token["jti"])
    return {
        "message":"logout successfully"
    }

