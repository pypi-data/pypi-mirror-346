from abc import ABC, abstractmethod


class AbsNonceRegistry(ABC):
    @abstractmethod
    async def register_nonce(self, nonce: bytes) -> bool:
        """True if nonce is fresh, False if reused"""
        pass
