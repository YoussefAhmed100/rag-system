from fastapi import FastAPI

from app.modules.base import router as base_router
from app.modules.upload import router as upload_router


app = FastAPI(
    title="RAG System",
)

app.include_router(base_router)
app.include_router(upload_router)