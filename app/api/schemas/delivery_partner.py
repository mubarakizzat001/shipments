from pydantic import EmailStr,BaseModel




class basedeliverypartner(BaseModel):
    name:str
    email:EmailStr
    max_handling_capacity:int
    servicable_zip_codes:list[int]

class deliverypartner_read(basedeliverypartner):
    pass


class deliverypartner_create(basedeliverypartner):
    password:str
  