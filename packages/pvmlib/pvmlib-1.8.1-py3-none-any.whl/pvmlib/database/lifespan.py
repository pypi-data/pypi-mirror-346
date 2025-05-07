from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import DatabaseManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await DatabaseManager.connect_to_mongo()
    except Exception as e:
        raise e
    yield
    await DatabaseManager.disconnect_from_mongo()