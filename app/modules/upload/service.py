from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

from app.core.config import Settings


class FileUploadService:

    def __init__(self, settings: Settings):
        self.settings = settings

        self.files_directory = (
            Path(__file__).resolve().parents[3]
            / "assets"
            / "files"
        )

    async def upload(
        self,
        project_id: str,
        file: UploadFile,
    ) -> str:

        project_directory = (
            self.files_directory / project_id
        )

        project_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_id = uuid4().hex

        safe_filename = self._sanitize_filename(
            file.filename
        )

        file_path = (
            project_directory
            / f"{file_id}_{safe_filename}"
        )

        await self._save_file(
            file=file,
            file_path=file_path,
        )

        return file_id

    async def _save_file(
        self,
        file: UploadFile,
        file_path: Path,
    ) -> None:

        async with aiofiles.open(
            file_path,
            "wb",
        ) as output_file:

            while chunk := await file.read(
                self.settings.FILE_DEFAULT_CHUNK_SIZE
            ):
                await output_file.write(chunk)

    def _sanitize_filename(
        self,
        filename: str,
    ) -> str:

        filename = Path(filename).name

        return "".join(
            character
            for character in filename
            if character.isalnum()
            or character in "._-"
        )