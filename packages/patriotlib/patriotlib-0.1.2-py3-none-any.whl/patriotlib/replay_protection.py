# patriotlib/replay_protection.py

import threading


class NonceRegistry:
    def __init__(self):
        self.seen = set()
        self.lock = threading.Lock()

    def register_nonce(self, nonce: bytes) -> bool:
        key = nonce.hex()
        with self.lock:
            if key in self.seen:
                return False
            self.seen.add(key)
            return True


nonce_registry = NonceRegistry()
