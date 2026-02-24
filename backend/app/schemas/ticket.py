# ABOUTME: Request/response schemas for tickets and messages.
# ABOUTME: Internal notes are never in parent-facing responses.

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.ticket import TicketCategory


class TicketCreate(BaseModel):
    student_ids: list[int] = Field(..., min_length=1)
    category: TicketCategory
    title: str | None = None
    description: str | None = None
    urgency: bool = False


class MessageIn(BaseModel):
    body: str = Field(..., min_length=1)


class InternalNoteIn(BaseModel):
    body: str = Field(..., min_length=1)


class ReopenIn(BaseModel):
    reason: str = Field(..., min_length=1)


class StatusUpdate(BaseModel):
    status: str  # "in_progress" | "resolved"


class KnownIssueUpdate(BaseModel):
    known_issue: bool


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_id: int
    sender_id: int
    body: str
    created_at: datetime
    is_staff: bool = False


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    school_id: int
    created_by_id: int
    category: TicketCategory
    status: str
    urgency: bool
    assigned_to_id: int | None
    title: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime
    student_ids: list[int] = []
    messages: list[MessageOut] = []
    internal_notes_count: int | None = None  # staff only; never content for parent
    satisfied_at: datetime | None = None
    transport_footer: str | None = None
    known_issue: bool = False
