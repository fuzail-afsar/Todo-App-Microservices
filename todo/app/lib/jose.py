from datetime import datetime, timedelta
from typing import Any

from jose import jwt

from app.core.config import settings


def create_access_token(data: dict, expires_delta: int = 15) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode = {"exp": expire, "data": data}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except:
        return None
