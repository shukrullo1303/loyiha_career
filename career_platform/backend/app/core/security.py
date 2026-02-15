from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(sub: str, role: str, expires_minutes: Optional[int] = None) -> str:
    if expires_minutes is None:
        expires_minutes = settings.ACCESS_TOKEN_MIN
    exp = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": sub, "role": role, "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

