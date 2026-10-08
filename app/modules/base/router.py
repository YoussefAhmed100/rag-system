from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings


router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@router.get("/")
async def welcome(
    settings: Settings = Depends(get_settings),
):
    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
    }