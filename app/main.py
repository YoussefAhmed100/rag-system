from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.config import get_settings
from app.core.database import Database

from app.modules.base import router as base_router
from app.modules.upload import router as upload_router
from app.modules.processing import router as processing_router


settings = get_settings()
database = Database(settings)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await database.connect()
        app.state.database = database.database

        print("MongoDB connection successful")

        yield
    finally:
        await database.close()


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)
app.include_router(base_router)
app.include_router(upload_router)
app.include_router(processing_router)