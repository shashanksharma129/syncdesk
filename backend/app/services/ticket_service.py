# ABOUTME: Ticket creation, reply, internal notes, and listing with visibility rules.
# ABOUTME: Staff reply auto-sets status to In Progress.

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import (
    InternalNote,
    Ticket,
    TicketCategory,
    TicketMessage,
    TicketReopen,
    TicketStatus,
    ticket_students,
)
from app.models.user import Role, User


async def create_ticket(
    session: AsyncSession,
    created_by: User,
    student_ids: list[int],
    category: TicketCategory,
    title: str | None,
    description: str | None,
    urgency: bool,
) -> Ticket:
    ticket = Ticket(
        school_id=created_by.school_id,
        created_by_id=created_by.id,
        category=category,
        status=TicketStatus.PENDING,
        urgency=urgency,
        title=title,
        description=description,
    )
    session.add(ticket)
    await session.flush()
    for sid in student_ids:
        await session.execute(insert(ticket_students).values(ticket_id=ticket.id, student_id=sid))
    await session.flush()
    return ticket


async def get_ticket_for_user(session: AsyncSession, ticket_id: int, user: User) -> Ticket | None:
    result = await session.execute(
        select(Ticket).where(Ticket.id == ticket_id, Ticket.deleted_at.is_(None))
    )
    ticket = result.scalar_one_or_none()
    if not ticket:
        return None
    if user.role == Role.PARENT:
        if ticket.created_by_id != user.id:
            return None
        return ticket
    if ticket.school_id != user.school_id:
        return None
    return ticket


async def list_tickets_for_user(session: AsyncSession, user: User) -> list[Ticket]:
    q = select(Ticket).where(
        Ticket.school_id == user.school_id,
        Ticket.deleted_at.is_(None),
    )
    if user.role == Role.PARENT:
        q = q.where(Ticket.created_by_id == user.id)
    q = q.order_by(Ticket.updated_at.desc())
    result = await session.execute(q)
    return list(result.scalars().all())


async def add_reply(
    session: AsyncSession,
    ticket_id: int,
    sender: User,
    body: str,
) -> TicketMessage | None:
    ticket = await get_ticket_for_user(session, ticket_id, sender)
    if not ticket:
        return None
    msg = TicketMessage(ticket_id=ticket_id, sender_id=sender.id, body=body)
    session.add(msg)
    await session.flush()
    is_staff = sender.role != Role.PARENT
    if is_staff and ticket.status == TicketStatus.PENDING:
        ticket.status = TicketStatus.IN_PROGRESS
        await session.flush()
    return msg


async def add_internal_note(
    session: AsyncSession,
    ticket_id: int,
    author: User,
    body: str,
) -> InternalNote | None:
    if author.role == Role.PARENT:
        return None
    ticket = await get_ticket_for_user(session, ticket_id, author)
    if not ticket:
        return None
    note = InternalNote(ticket_id=ticket_id, author_id=author.id, body=body)
    session.add(note)
    await session.flush()
    return note


async def get_ticket_messages(session: AsyncSession, ticket_id: int) -> list[TicketMessage]:
    result = await session.execute(
        select(TicketMessage).where(TicketMessage.ticket_id == ticket_id).order_by(TicketMessage.created_at)
    )
    return list(result.scalars().all())


async def get_internal_notes_count(session: AsyncSession, ticket_id: int) -> int:
    from sqlalchemy import func
    result = await session.execute(
        select(func.count(InternalNote.id)).where(InternalNote.ticket_id == ticket_id)
    )
    return result.scalar() or 0


async def get_ticket_student_ids(session: AsyncSession, ticket_id: int) -> list[int]:
    result = await session.execute(
        select(ticket_students.c.student_id).where(ticket_students.c.ticket_id == ticket_id)
    )
    return [r[0] for r in result.all()]


async def get_parent_student_ids(session: AsyncSession, parent_id: int) -> list[int]:
    from app.models.student import parent_students
    result = await session.execute(
        select(parent_students.c.student_id).where(parent_students.c.parent_id == parent_id)
    )
    return [r[0] for r in result.all()]


MAX_REOPEN_PER_TICKET = 2


async def request_reopen(
    session: AsyncSession,
    ticket_id: int,
    user: User,
    reason: str,
) -> TicketReopen | None:
    ticket = await get_ticket_for_user(session, ticket_id, user)
    if not ticket or ticket.status != TicketStatus.RESOLVED:
        return None
    if user.role != Role.PARENT:
        return None
    result = await session.execute(
        select(func.count(TicketReopen.id)).where(TicketReopen.ticket_id == ticket_id)
    )
    if (result.scalar() or 0) >= MAX_REOPEN_PER_TICKET:
        return None
    reopen = TicketReopen(ticket_id=ticket_id, requested_by_id=user.id, reason=reason)
    session.add(reopen)
    await session.flush()
    ticket.status = TicketStatus.PENDING
    ticket.satisfied_at = None
    await session.flush()
    return reopen


async def set_ticket_known_issue(
    session: AsyncSession,
    ticket_id: int,
    user: User,
    known_issue: bool,
) -> bool:
    if user.role != Role.TRANSPORT:
        return False
    ticket = await get_ticket_for_user(session, ticket_id, user)
    if not ticket or ticket.category != TicketCategory.TRANSPORT:
        return False
    ticket.known_issue = known_issue
    await session.flush()
    return True


async def set_ticket_status(
    session: AsyncSession,
    ticket_id: int,
    user: User,
    new_status: TicketStatus,
) -> bool:
    if user.role == Role.PARENT:
        return False
    ticket = await get_ticket_for_user(session, ticket_id, user)
    if not ticket:
        return False
    ticket.status = new_status
    await session.flush()
    return True


async def mark_satisfied(
    session: AsyncSession,
    ticket_id: int,
    user: User,
) -> bool:
    ticket = await get_ticket_for_user(session, ticket_id, user)
    if not ticket or ticket.status != TicketStatus.RESOLVED:
        return False
    if user.role != Role.PARENT or ticket.created_by_id != user.id:
        return False
    from datetime import datetime, timezone
    ticket.satisfied_at = datetime.now(timezone.utc)
    await session.flush()
    return True
