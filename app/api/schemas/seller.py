from pydantic import EmailStr,BaseModel




class base_seller(BaseModel):
    name:str
    email:EmailStr

class seller_read(base_seller):
    pass


class seller_create(base_seller):
    password:str