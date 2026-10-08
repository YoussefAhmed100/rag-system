from fastapi import UploadFile

from app.core.config import Settings


class FileValidator:

    def __init__(self, settings: Settings):
        self.settings = settings

    def validate(self, file: UploadFile) -> None:

        if not file.filename:
            raise ValueError("File name is required")

        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            raise ValueError("File type is not supported")

        if file.size is not None:
            max_size = self.settings.FILE_MAX_SIZE * 1024 * 1024

            if file.size > max_size:
                raise ValueError("File size exceeded")