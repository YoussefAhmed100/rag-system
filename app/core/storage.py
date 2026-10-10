
from pathlib import Path


def get_files_directory() -> Path:
    return (
        Path(__file__).resolve().parents[2]
        / "assets"
        / "files"
    ).resolve()
