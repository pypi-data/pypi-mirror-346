import hashlib
import redis.asyncio as aioredis
from patriotlib.interfaces import AbsNonceRegistry


class AioredisNonceRegistry(AbsNonceRegistry):
    def __init__(self, redis_url="redis://localhost:6379", ttl_seconds=300):
        self.client = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        self.ttl = ttl_seconds

    async def register_nonce(self, nonce: bytes) -> bool:
        key = "nonce:" + hashlib.sha256(nonce).hexdigest()
        return bool(await self.client.set(key, "1", nx=True, ex=self.ttl))
