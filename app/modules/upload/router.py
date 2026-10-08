from fastapi import APIRouter, Depends, UploadFile

from app.core.config import Settings, get_settings
from .controller import UploadController


router = APIRouter(
    prefix="/api/v1/data",
    tags=["data"],
)


@router.post("/upload/{project_id}")
async def upload_file(
    project_id: str,
    file: UploadFile,
    settings: Settings = Depends(get_settings),
):
    controller = UploadController(settings)

    file_id = await controller.upload_file(
        project_id=project_id,
        file=file,
    )

    return {
        "signal": "file_upload_success",
        "file_id": file_id,
    }