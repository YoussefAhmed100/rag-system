from fastapi import UploadFile

from app.core.config import Settings
from .service import FileUploadService
from .validator import FileValidator


class UploadController:

    def __init__(self, settings: Settings):
        self.validator = FileValidator(settings)
        self.service = FileUploadService(settings)

    async def upload_file(
        self,
        project_id: str,
        file: UploadFile,
    ) -> str:

        self.validator.validate(file)

        file_id = await self.service.upload(
            project_id=project_id,
            file=file,
        )

        return file_id