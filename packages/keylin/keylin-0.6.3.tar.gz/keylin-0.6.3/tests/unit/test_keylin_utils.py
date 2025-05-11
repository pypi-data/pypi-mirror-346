import uuid

from keylin.config import Settings
from keylin.keylin_utils import create_jwt_for_user


def test_create_jwt_for_user():
    user_id = uuid.uuid4()
    email = "test@example.com"
    token = create_jwt_for_user(user_id, email)
    assert isinstance(token, str)
    # Optionally, decode and check claims
    import jwt

    settings = Settings()
    payload = jwt.decode(
        token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )
    assert payload["sub"] == str(user_id)
    assert payload["email"] == email
    assert "exp" in payload
    assert "iat" in payload
