# ABOUTME: Transport broadcast rate limit: one per route per 2 hours.

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TransportBroadcast(Base):
    __tablename__ = "transport_broadcasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    route_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    last_broadcast_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
