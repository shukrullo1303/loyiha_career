import base64
from typing import Optional

from cryptography.fernet import Fernet

from app.core.config import settings


def _fernet() -> Fernet:
    # FIELD_KEY 32-byte raw key -> urlsafe base64 for Fernet
    raw = settings.FIELD_KEY.encode("utf-8")[:32].ljust(32, b"_")
    key = base64.urlsafe_b64encode(raw)
    return Fernet(key)


def encrypt_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    return _fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    return _fernet().decrypt(value.encode("utf-8")).decode("utf-8")

