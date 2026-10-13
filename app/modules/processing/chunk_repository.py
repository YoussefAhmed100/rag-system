
from pymongo import ASCENDING
from pymongo.asynchronous.database import AsyncDatabase


class ChunkRepository:
    def __init__(self, database: AsyncDatabase) -> None:
        self.collection = database["chunks"]

    async def create_indexes(self) -> None:
        await self.collection.create_index(
            [
                ("project_id", ASCENDING),
                ("file_id", ASCENDING),
                ("chunk_index", ASCENDING),
            ],
            unique=True,
            name="unique_file_chunk",
        )

        await self.collection.create_index(
            [
                ("project_id", ASCENDING),
                ("file_id", ASCENDING),
            ],
            name="project_file_lookup",
        )

    async def replace_file_chunks(
        self,
        project_id: str,
        file_id: str,
        chunks: list[dict],
    ) -> int:
        await self.collection.delete_many(
            {
                "project_id": project_id,
                "file_id": file_id,
            }
        )

        if not chunks:
            return 0

        await self.collection.insert_many(chunks)

        return len(chunks)