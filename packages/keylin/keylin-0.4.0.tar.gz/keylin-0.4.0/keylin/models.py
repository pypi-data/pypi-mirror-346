import uuid
from datetime import UTC, datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):  # type: ignore[misc, valid-type]
    __tablename__ = "user"
    full_name = Column(String, nullable=True)


class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    key_hash = Column(String, nullable=False, unique=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now(UTC))
    service_id = Column(String, nullable=False)
    status = Column(String, default="active")
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)

    def __init__(
        self,
        user_id: str,
        key_hash: str,
        service_id: str,
        name: str | None = None,
        status: str = "active",
        expires_at: datetime | None = None,
        last_used_at: datetime | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
    ):
        if not service_id:
            raise ValueError("service_id is required for APIKey")
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.key_hash = key_hash
        self.name = name
        self.created_at = created_at or datetime.now(UTC)
        self.service_id = service_id
        self.status = status
        self.expires_at = expires_at
        self.last_used_at = last_used_at
