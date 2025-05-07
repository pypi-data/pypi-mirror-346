# patriotlib/crypto.py

import os
import json
import base64
from cryptography.hazmat.primitives import padding, hmac, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from patriotlib.replay_registry import get_nonce_registry


def _require_key_length(key):
    if len(key) != 32:
        raise ValueError("Invalid key length: expected 32 bytes")


async def encrypt(key, plaintext: bytes) -> bytes:
    _require_key_length(key)
    iv = os.urandom(16)
    nonce = os.urandom(12)

    inner = {
        "nonce": base64.b64encode(nonce).decode(),
        "payload": base64.b64encode(plaintext).decode()
    }
    inner_bytes = json.dumps(inner).encode()

    padder = padding.PKCS7(128).padder()
    padded = padder.update(inner_bytes) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    ciphertext = cipher.encryptor().update(padded) + cipher.encryptor().finalize()

    mac = hmac.HMAC(key, hashes.SHA256())
    mac.update(iv + ciphertext)
    return iv + ciphertext + mac.finalize()


async def decrypt(key, data: bytes) -> bytes:
    _require_key_length(key)
    iv, ciphertext, tag = data[:16], data[16:-32], data[-32:]

    mac = hmac.HMAC(key, hashes.SHA256())
    mac.update(iv + ciphertext)
    mac.verify(tag)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    padded = cipher.decryptor().update(ciphertext) + cipher.decryptor().finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(padded) + unpadder.finalize()

    inner = json.loads(decrypted)
    nonce = base64.b64decode(inner["nonce"])
    payload = base64.b64decode(inner["payload"])

    if not await get_nonce_registry().register_nonce(nonce):
        raise ValueError("Replay attack detected")

    return payload
