
from fastapi import HTTPException, status

from app.modules.processing.dto import ProcessRequest
from app.modules.processing.service import ProcessingService


class ProcessingController:
    def __init__(self):
        self.service = ProcessingService()

    def process_file(
        self,
        project_id: str,
        request: ProcessRequest,
    ) -> dict:
        try:
            chunks = self.service.process_file(
                project_id=project_id,
                request=request,
            )

            if not chunks:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="No text content could be extracted from the file",
                )

            return {
                "signal": "file_processing_success",
                "project_id": project_id,
                "file_id": request.file_id,
                "chunks_count": len(chunks),
                "chunks": [
                    {
                        "content": chunk.page_content,
                        "metadata": chunk.metadata,
                    }
                    for chunk in chunks
                ],
            }

        except FileNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during file processing",
            ) from exc