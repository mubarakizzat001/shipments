### shipment management api

from ml_fastapi.database.session import create_db_table
from ml_fastapi.api.router import router
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_table()
    yield


### create fastapi app
app = FastAPI(lifespan=lifespan_handler)


app.include_router(router)

### scalar endpoint
@app.get("/scalar",include_in_schema=False)
def scalar_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar FastAPI Example"

    )