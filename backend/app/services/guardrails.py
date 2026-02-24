# ABOUTME: Ticket creation guardrails: open count, cooldown, 7-day cap, one open Other.
# ABOUTME: Returns user-friendly error message or None if allowed.

from datetime import datetime, timezone, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket, TicketCategory, TicketStatus
from app.models.user import Role, User

MAX_OPEN_TICKETS = 3
COOLDOWN_MINUTES = 30
MAX_TICKETS_7_DAYS = 5
MAX_OPEN_OTHER = 1


URGENT_ALLOWED_CATEGORIES = (TicketCategory.TRANSPORT, TicketCategory.HEALTH_SAFETY)


async def check_guardrails(
    session: AsyncSession,
    created_by: User,
    category: TicketCategory,
    urgency: bool = False,
) -> str | None:
    if created_by.role != Role.PARENT:
        return None
    now = datetime.now(timezone.utc)
    until_blocked = getattr(created_by, "ticket_creation_blocked_until", None)
    if until_blocked:
        ut = until_blocked.replace(tzinfo=timezone.utc) if until_blocked.tzinfo is None else until_blocked
        if ut > now:
            return "Ticket creation is temporarily unavailable. Please contact the school office."
    open_statuses = (TicketStatus.PENDING, TicketStatus.IN_PROGRESS)

    result = await session.execute(
        select(func.count(Ticket.id)).where(
            Ticket.created_by_id == created_by.id,
            Ticket.school_id == created_by.school_id,
            Ticket.status.in_(open_statuses),
        )
    )
    open_count = result.scalar() or 0
    if open_count >= MAX_OPEN_TICKETS:
        return "You already have the maximum number of open tickets. Please wait for existing tickets to be resolved before creating a new one."

    result = await session.execute(
        select(func.max(Ticket.created_at)).where(
            Ticket.created_by_id == created_by.id,
        )
    )
    last_created = result.scalar()
    if last_created:
        if last_created.tzinfo is None:
            last_created = last_created.replace(tzinfo=timezone.utc)
        if (now - last_created).total_seconds() < COOLDOWN_MINUTES * 60:
            return "Please wait a few minutes between creating tickets. You can try again shortly."

    seven_days_ago = now - timedelta(days=7)
    result = await session.execute(
        select(func.count(Ticket.id)).where(
            Ticket.created_by_id == created_by.id,
            Ticket.created_at >= seven_days_ago,
        )
    )
    recent_count = result.scalar() or 0
    if recent_count >= MAX_TICKETS_7_DAYS:
        return "You have reached the limit of tickets per week. Please wait until next week or contact the school office."

    if category == TicketCategory.OTHER:
        result = await session.execute(
            select(func.count(Ticket.id)).where(
                Ticket.created_by_id == created_by.id,
                Ticket.school_id == created_by.school_id,
                Ticket.category == TicketCategory.OTHER,
                Ticket.status.in_(open_statuses),
            )
        )
        open_other = result.scalar() or 0
        if open_other >= MAX_OPEN_OTHER:
            return "You already have an open ticket in the \"Other\" category. Please wait for it to be resolved before creating another."

    if urgency:
        if category not in URGENT_ALLOWED_CATEGORIES:
            return "Urgent tickets are only allowed for Transport and Health & Safety."
        seven_days_ago = now - timedelta(days=7)
        result = await session.execute(
            select(func.count(Ticket.id)).where(
                Ticket.created_by_id == created_by.id,
                Ticket.urgency.is_(True),
                Ticket.created_at >= seven_days_ago,
            )
        )
        urgent_count = result.scalar() or 0
        if urgent_count >= 1:
            return "You may only have one urgent ticket per week."

    return None
