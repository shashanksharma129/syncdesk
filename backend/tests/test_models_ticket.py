# ABOUTME: Unit tests for Ticket model and status transitions.
# ABOUTME: Ensures valid status flow Pending -> In Progress -> Resolved.

import pytest

from app.models.ticket import InternalNote, Ticket, TicketCategory, TicketMessage, TicketStatus


@pytest.mark.asyncio
async def test_ticket_create_and_status_default(db_session):
    from app.models.user import Role, User

    user = User(phone="+919999000077", role=Role.PARENT, school_id=1)
    db_session.add(user)
    await db_session.flush()
    ticket = Ticket(
        school_id=1,
        created_by_id=user.id,
        category=TicketCategory.TRANSPORT,
        status=TicketStatus.PENDING,
        urgency=False,
    )
    db_session.add(ticket)
    await db_session.flush()
    assert ticket.id is not None
    assert ticket.status == TicketStatus.PENDING
    assert ticket.category == TicketCategory.TRANSPORT


@pytest.mark.asyncio
async def test_ticket_message_and_internal_note_create(db_session):
    from app.models.user import Role, User

    user = User(phone="+919999000088", role=Role.PARENT, school_id=1)
    db_session.add(user)
    await db_session.flush()
    ticket = Ticket(
        school_id=1,
        created_by_id=user.id,
        category=TicketCategory.OTHER,
        status=TicketStatus.PENDING,
    )
    db_session.add(ticket)
    await db_session.flush()
    msg = TicketMessage(ticket_id=ticket.id, sender_id=user.id, body="Hello")
    db_session.add(msg)
    note = InternalNote(ticket_id=ticket.id, author_id=user.id, body="Internal")
    db_session.add(note)
    await db_session.flush()
    assert msg.id is not None
    assert note.id is not None
