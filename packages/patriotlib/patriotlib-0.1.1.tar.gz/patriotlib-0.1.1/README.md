# PatriotLib 🇷🇺

📦 PatriotLib — это библиотека криптографической защиты, разработанная для защищённой передачи, подписи и расшифровки данных в клиент-серверной архитектуре.

## Возможности

- AES-256 (CBC + HMAC-SHA256) для симметричного шифрования
- Поддержка ECDH для безопасного обмена ключами
- Подпись и проверка сообщений (ECDSA P-384)
- Защита от replay-атак через nonce
- Полное покрытие юнит-тестами

## Установка

pip install patriotlib

## Пример использования

## Example

```python
from patriotlib.crypto import encrypt, decrypt
from patriotlib.keyexchange import generate_ecdh_keys, derive_shared_key

# ECDH exchange, derive shared key
client_priv, client_pub = generate_ecdh_keys()
server_priv, server_pub = generate_ecdh_keys()
shared_key = derive_shared_key(client_priv, server_pub)

# Encrypt / Decrypt
cipher = await encrypt(shared_key, b"Top Secret")
plain = await decrypt(shared_key, cipher)