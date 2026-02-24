# ABOUTME: Request/response schemas for announcements.

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AnnouncementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    target_audience: str = Field(..., pattern="^(parents|staff|both)$")
    target_grade: str | None = None
    target_class: str | None = None


class AnnouncementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    school_id: int
    author_id: int
    title: str
    content: str
    target_audience: str
    target_grade: str | None
    target_class: str | None
    created_at: datetime
    read: bool = False
