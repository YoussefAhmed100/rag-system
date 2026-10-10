
import logging
import re
from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import HTTPException, UploadFile, status

from app.core.config import Settings
from app.core.storage import get_files_directory


logger = logging.getLogger(__name__)


class FileUploadService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.files_directory = get_files_directory()

    async def upload(
        self,
        project_id: str,
        file: UploadFile,
    ) -> str:
        self._validate_project_id(project_id)
        filename = self._get_safe_filename(file.filename)
        project_directory = self._get_project_directory(project_id)

        file_id = uuid4().hex
        temporary_path = project_directory / f".{file_id}.part"
        final_path = project_directory / f"{file_id}_{filename}"

        try:
            project_directory.mkdir(parents=True, exist_ok=True)

            await self._save_file(file, temporary_path)
            temporary_path.replace(final_path)

            logger.info(
                "File uploaded successfully: project_id=%s file_id=%s",
                project_id,
                file_id,
            )
            return file_id

        except HTTPException:
            self._remove_temporary_file(temporary_path)
            raise

        except OSError as exc:
            self._remove_temporary_file(temporary_path)
            logger.exception("File storage operation failed")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to save the file. Please try again later.",
            ) from exc

        except Exception:
            self._remove_temporary_file(temporary_path)
            logger.exception("Unexpected error during file upload")
            raise

    async def _save_file(
        self,
        file: UploadFile,
        file_path: Path,
    ) -> None:
        total_size = 0
        max_size = self.settings.FILE_MAX_SIZE
        chunk_size = self.settings.FILE_DEFAULT_CHUNK_SIZE

        try:
            async with aiofiles.open(file_path, "wb") as output_file:
                while True:
                    chunk = await file.read(chunk_size)

                    if not chunk:
                        break

                    total_size += len(chunk)
                    self._validate_file_size(total_size, max_size)

                    await output_file.write(chunk)

        except HTTPException:
            raise

        except OSError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to save the file. Please try again later.",
            ) from exc

    @staticmethod
    def _validate_project_id(project_id: str) -> None:
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", project_id or ""):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid project_id. Use 1-100 letters, "
                    "numbers, underscores or hyphens."
                ),
            )

    @staticmethod
    def _get_safe_filename(filename: str | None) -> str:
        original_name = Path(
            (filename or "").replace("\\", "/")
        ).name

        if not original_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A valid filename is required.",
            )

        safe_name = "".join(
            character
            for character in original_name
            if character.isalnum() or character in "._-"
        ).strip(".")

        if not safe_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The provided filename is invalid.",
            )

        return safe_name[:200]

    def _get_project_directory(self, project_id: str) -> Path:
        project_directory = (
            self.files_directory / project_id
        ).resolve()

        if project_directory.parent != self.files_directory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid project_id.",
            )

        return project_directory

    @staticmethod
    def _validate_file_size(
        total_size: int,
        max_size: int,
    ) -> None:
        if total_size > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=(
                    f"File exceeds the maximum allowed size "
                    f"of {max_size} bytes."
                ),
            )

    @staticmethod
    def _remove_temporary_file(file_path: Path) -> None:
        try:
            file_path.unlink(missing_ok=True)
        except OSError:
            logger.exception("Failed to remove temporary upload file")