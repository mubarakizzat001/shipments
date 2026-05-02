from pydantic import EmailStr,BaseModel,Field




class BaseDeliveryPartner(BaseModel):
    name:str
    email:EmailStr
    max_handling_capacity:int
    servicable_zip_codes:list[int]

class DeliveryPartner_Read(BaseDeliveryPartner):
    pass

class DeliveryPartner_Update(BaseModel):
    max_handling_capacity:int | None=Field(default=None)
    servicable_zip_codes:list[int] | None=Field(default=None)

class DeliveryPartner_Create(BaseDeliveryPartner):
    password:str
  