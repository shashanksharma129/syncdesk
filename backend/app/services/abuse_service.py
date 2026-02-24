# ABOUTME: Abuse flag on ticket, list flagged for director, restrict/block parent.
# ABOUTME: Director-only actions for restrict and block.

from datetime import datetime, timezone, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.models.user import Role, User


async def flag_abuse(
    session: AsyncSession,
    ticket_id: int,
    staff: User,
) -> Ticket | None:
    if staff.role == Role.PARENT:
        return None
    result = await session.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket or ticket.school_id != staff.school_id:
        return None
    ticket.abuse_flagged = True
    ticket.abuse_flagged_at = datetime.now(timezone.utc)
    ticket.abuse_flagged_by_id = staff.id
    await session.flush()
    return ticket


async def list_abuse_flagged(session: AsyncSession, school_id: int) -> list[Ticket]:
    result = await session.execute(
        select(Ticket).where(
            Ticket.school_id == school_id,
            Ticket.abuse_flagged.is_(True),
            Ticket.deleted_at.is_(None),
        ).order_by(Ticket.abuse_flagged_at.desc())
    )
    return list(result.scalars().all())


async def restrict_parent_to_admin(
    session: AsyncSession,
    parent_id: int,
    director: User,
    duration_days: int = 7,
) -> User | None:
    if director.role != Role.DIRECTOR:
        return None
    result = await session.execute(select(User).where(User.id == parent_id))
    user = result.scalar_one_or_none()
    if not user or user.role != Role.PARENT or user.school_id != director.school_id:
        return None
    user.restricted_to_admin_until = datetime.now(timezone.utc) + timedelta(days=duration_days)
    await session.flush()
    return user


async def block_parent_ticket_creation(
    session: AsyncSession,
    parent_id: int,
    director: User,
    duration_days: int = 3,
) -> User | None:
    if director.role != Role.DIRECTOR:
        return None
    result = await session.execute(select(User).where(User.id == parent_id))
    user = result.scalar_one_or_none()
    if not user or user.role != Role.PARENT or user.school_id != director.school_id:
        return None
    user.ticket_creation_blocked_until = datetime.now(timezone.utc) + timedelta(days=duration_days)
    await session.flush()
    return user
