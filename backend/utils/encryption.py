import os
from cryptography.fernet import Fernet


def get_cipher() -> Fernet:
    key = os.getenv("ENCRYPTION_KEY", "")
    if not key:
        raise RuntimeError(
            "ENCRYPTION_KEY not set. Run python utils/generate_keys.py to generate one."
        )
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt(text: str) -> str:
    return get_cipher().encrypt(text.encode()).decode()


def decrypt(token: str) -> str:
    return get_cipher().decrypt(token.encode()).decode()


def generate_key() -> str:
    return Fernet.generate_key().decode()
