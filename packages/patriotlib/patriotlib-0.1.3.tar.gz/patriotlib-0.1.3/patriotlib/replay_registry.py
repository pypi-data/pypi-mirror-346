# patriotlib/replay_registry.py

from patriotlib.interfaces import AbsNonceRegistry
from patriotlib.replay_protection.memory_async import InMemoryNonceRegistry

_nonce_registry: AbsNonceRegistry = InMemoryNonceRegistry()


def get_nonce_registry() -> AbsNonceRegistry:
    return _nonce_registry


def set_nonce_registry(registry: AbsNonceRegistry):
    global _nonce_registry
    _nonce_registry = registry
