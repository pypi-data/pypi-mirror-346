# keylin/jwt_utils.py

import uuid
from datetime import UTC, datetime, timedelta

import jwt

from .config import Settings

settings = Settings()


def create_jwt_for_user(
    user_id: uuid.UUID,
    email: str,
    expires_seconds: int = 3600,
    settings: Settings | None = None,
) -> str:
    """
    Create a JWT for a test user.

    Args:
        user_id (uuid.UUID): The user ID.
        email (str): The user's email.
        expires_seconds (int): Expiry in seconds.
        settings (Settings): The settings instance to use.

    Returns:
        str: Encoded JWT token.
    """
    settings = settings or Settings()
    now = datetime.now(UTC)
    exp = now + timedelta(seconds=expires_seconds or settings.JWT_EXPIRE_SECONDS)
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": exp,
        "iat": now,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
