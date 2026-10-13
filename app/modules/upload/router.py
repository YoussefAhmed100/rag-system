
from fastapi import APIRouter, Depends, Request, UploadFile

from app.core.config import Settings, get_settings
from app.modules.processing.chunk_repository import ChunkRepository
from .controller import UploadController


router = APIRouter(
    prefix="/api/v1/data",
    tags=["data"],
)


@router.post("/upload/{project_id}")
async def upload_file(
    request: Request,
    project_id: str,
    file: UploadFile,
    settings: Settings = Depends(get_settings),
) -> dict[str, str | int]:
    chunk_repository: ChunkRepository = (
        request.app.state.chunk_repository
    )

    controller = UploadController(
        settings=settings,
        chunk_repository=chunk_repository,
    )

    return await controller.upload_file(
        project_id=project_id,
        file=file,
    )