from fastapi import FastAPI
import psycopg2

from router import organizations
from src.db import models
from src.db.database import engine
from router import applications
from router import services
from src.app.middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_pagination import add_pagination



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
app.include_router(organizations.router)
app.include_router(applications.router)
app.include_router(services.router)

@app.get("/health/")
async def ping():
    return {"message": "up"}

add_pagination(app)