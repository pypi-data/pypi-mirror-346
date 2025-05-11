import uuid
from datetime import UTC, datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, DateTime, ForeignKey, Index, String, event
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):  # type: ignore[misc, valid-type]
    __tablename__ = "user"
    full_name = Column(String, nullable=True)
    user_id_str = Column(String(36), unique=True, nullable=False)


@event.listens_for(User, "before_insert")
def set_user_id_str(mapper, connection, target):
    if not target.id:
        target.id = uuid.uuid4()
    target.user_id_str = str(target.id)


class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # Use user_id as the foreign key for cross-database compatibility
    user_id = Column(
        String(36), ForeignKey("user.user_id_str", ondelete="CASCADE"), nullable=False
    )
    key_hash = Column(String, nullable=False, unique=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now(UTC))
    service_id = Column(String, nullable=False)
    status = Column(String, default="active")
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    __table_args__ = (Index("ix_api_keys_user_id", "user_id"),)

    def __init__(
        self,
        user_id: str,  # Now expects string version of user id
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
