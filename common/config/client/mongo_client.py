from motor.motor_asyncio import AsyncIOMotorClient

from common.config.settings import settings

mongo_client = AsyncIOMotorClient(settings.MONGODB_URI)
