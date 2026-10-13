
import logging

from fastapi import HTTPException, UploadFile, status

from app.core.config import Settings
from app.modules.processing.chunk_repository import ChunkRepository
from app.modules.processing.dto import ProcessRequest
from app.modules.processing.service import ProcessingService
from app.modules.upload.service import FileUploadService


logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(
        self,
        settings: Settings,
        chunk_repository: ChunkRepository,
    ) -> None:
        self.upload_service = FileUploadService(settings)
        self.processing_service = ProcessingService()
        self.chunk_repository = chunk_repository

    async def ingest(
        self,
        project_id: str,
        file: UploadFile,
    ) -> dict[str, str | int]:
        file_id = await self.upload_service.upload(
            project_id=project_id,
            file=file,
        )

        request = ProcessRequest(file_id=file_id)

        chunks = self.processing_service.process_file(
            project_id=project_id,
            request=request,
        )

        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No text content could be extracted from the file.",
            )

        source_filename = file.filename or "unknown"

        chunk_documents = [
            {
                "project_id": project_id,
                "file_id": file_id,
                "chunk_index": index,
                "text": chunk.page_content,
                "metadata": {
                    **chunk.metadata,
                    "source": source_filename,
                },
            }
            for index, chunk in enumerate(chunks)
        ]

        saved_count = await self.chunk_repository.replace_file_chunks(
            project_id=project_id,
            file_id=file_id,
            chunks=chunk_documents,
        )

        logger.info(
            "File ingestion completed: project_id=%s file_id=%s chunks=%s",
            project_id,
            file_id,
            saved_count,
        )

        return {
            "project_id": project_id,
            "file_id": file_id,
            "chunks_count": saved_count,
        }