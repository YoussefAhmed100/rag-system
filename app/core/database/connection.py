from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import Settings


class Database:
    def __init__(self, settings: Settings) -> None:
        self.client = AsyncMongoClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000,
        )
        self.database: AsyncDatabase = self.client[
            settings.MONGODB_DATABASE
        ]

    async def connect(self) -> None:
        await self.client.admin.command("ping")

    async def close(self) -> None:
        await self.client.close()