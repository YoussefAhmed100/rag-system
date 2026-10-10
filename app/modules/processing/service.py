
import logging
import re
from pathlib import Path

from fastapi import HTTPException, status
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.storage import get_files_directory
from app.modules.processing.dto import ProcessRequest
from app.modules.processing.enums import SupportedFileExtension


logger = logging.getLogger(__name__)


class ProcessingService:
    def __init__(self) -> None:
        self.files_directory = get_files_directory()

    def process_file(
        self,
        project_id: str,
        request: ProcessRequest,
    ) -> list[Document]:
        self._validate_identifiers(project_id, request.file_id)

        project_directory = self._get_project_directory(project_id)
        file_path = self._find_file(
            project_directory,
            request.file_id,
        )

        documents = self._load_file(file_path)

        return self._split_documents(
            documents=documents,
            chunk_size=request.chunk_size,
            overlap_size=request.overlap_size,
        )

    @staticmethod
    def _validate_identifiers(
        project_id: str,
        file_id: str,
    ) -> None:
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", project_id or ""):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid project_id.",
            )

        if not re.fullmatch(r"[a-fA-F0-9]{32}", file_id or ""):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file_id.",
            )

    def _get_project_directory(self, project_id: str) -> Path:
        project_directory = (
            self.files_directory / project_id
        ).resolve()

        if project_directory.parent != self.files_directory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid project path.",
            )

        if not project_directory.is_dir():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        return project_directory

    def _find_file(
        self,
        project_directory: Path,
        file_id: str,
    ) -> Path:
        matches = list(project_directory.glob(f"{file_id}_*"))

        if not matches:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found.",
            )

        if len(matches) > 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Multiple files found for this file_id.",
            )

        file_path = matches[0].resolve()

        if (
            file_path.parent != project_directory
            or not file_path.is_file()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file path.",
            )

        if not self._is_supported_file(file_path):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Unsupported file type. Only PDF and TXT are supported.",
            )

        return file_path

    @staticmethod
    def _is_supported_file(file_path: Path) -> bool:
        return file_path.suffix.lower() in {
            extension.value
            for extension in SupportedFileExtension
        }

    def _load_file(self, file_path: Path) -> list[Document]:
        loader = self._get_loader(file_path)

        try:
            documents = loader.load()
        except (OSError, ValueError) as exc:
            logger.warning(
                "Failed to read uploaded file: %s",
                file_path.name,
                exc_info=True,
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unable to read the file. It may be corrupted or invalid.",
            ) from exc

        if not any(document.page_content.strip() for document in documents):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No readable text found in the file.",
            )

        return documents

    @staticmethod
    def _get_loader(file_path: Path):
        extension = file_path.suffix.lower()

        if extension == SupportedFileExtension.TXT.value:
            return TextLoader(
                str(file_path),
                encoding="utf-8",
            )

        if extension == SupportedFileExtension.PDF.value:
            return PyMuPDFLoader(str(file_path))

        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Only PDF and TXT are supported.",
        )

    @staticmethod
    def _split_documents(
        documents: list[Document],
        chunk_size: int,
        overlap_size: int,
    ) -> list[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        return splitter.split_documents(documents)