from fastapi import FastAPI
from services.catalog.app.api.router import router

app = FastAPI()

app.include_router(router, prefix="/api/v1", tags=["v11"])
