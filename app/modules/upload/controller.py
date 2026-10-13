
from fastapi import UploadFile

from app.core.config import Settings
from app.modules.processing.chunk_repository import ChunkRepository
from app.modules.ingestion import IngestionService
from .validator import FileValidator


class UploadController:
    def __init__(
        self,
        settings: Settings,
        chunk_repository: ChunkRepository,
    ) -> None:
        self.validator = FileValidator(settings)
        self.ingestion_service = IngestionService(
            settings=settings,
            chunk_repository=chunk_repository,
        )

    async def upload_file(
        self,
        project_id: str,
        file: UploadFile,
    ) -> dict[str, str | int]:
        self.validator.validate(file)

        result = await self.ingestion_service.ingest(
            project_id=project_id,
            file=file,
        )

        return {
            "signal": "file_ingestion_success",
            **result,
        }