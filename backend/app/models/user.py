# ABOUTME: User and OTP SQLAlchemy models for identity and auth.
# ABOUTME: User has role and school_id; OTP stores hashed code and expiry.

import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Role(str, enum.Enum):
    DIRECTOR = "director"
    PRINCIPAL = "principal"
    VICE_PRINCIPAL = "vice_principal"
    TEACHER = "teacher"
    OFFICE = "office"
    TRANSPORT = "transport"
    PARENT = "parent"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    school_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    restricted_to_admin_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ticket_creation_blocked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class OTP(Base):
    __tablename__ = "otps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    hashed_code: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
