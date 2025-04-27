import redis.asyncio as redis
from ..core.config import settings

class RedisService:
    def __init__(self):
        self.redis = redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
            decode_responses=True
        )

    async def set(self, key: str, value: str, ttl: int = 300):
        await self.redis.set(key, value, ex=ttl)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)
