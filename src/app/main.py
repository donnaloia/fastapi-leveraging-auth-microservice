from fastapi import FastAPI
import psycopg2

from src.db import models
from src.db.database import engine
from src.router import items, categories
from src.app.middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_pagination import add_pagination



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
app.include_router(categories.router)
app.include_router(items.router)

@app.get("/ping/")
async def ping():
    return {"message": "pong"}

add_pagination(app)