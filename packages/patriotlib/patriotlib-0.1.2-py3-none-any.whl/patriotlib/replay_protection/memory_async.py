from patriotlib.interfaces import AbsNonceRegistry
import asyncio


class InMemoryNonceRegistry(AbsNonceRegistry):
    def __init__(self):
        self.seen = set()
        self.lock = asyncio.Lock()

    async def register_nonce(self, nonce: bytes) -> bool:
        key = nonce.hex()
        async with self.lock:
            if key in self.seen:
                return False
            self.seen.add(key)
            return True
