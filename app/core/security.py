from fastapi.security import OAuth2PasswordBearer


OAuth_schemas_seller=OAuth2PasswordBearer(tokenUrl="/seller/login")
OAuth_schemas_deliverypartner=OAuth2PasswordBearer(tokenUrl="/deliverypartner/login")
