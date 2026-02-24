# ABOUTME: Tests for ticket creation guardrails: open count, cooldown, 7-day cap, Other, urgent.
# ABOUTME: Each guardrail returns a user-friendly message when violated.

import uuid
from datetime import datetime, timezone, timedelta

import pytest

from app.models.ticket import Ticket, TicketCategory, TicketStatus, ticket_students
from app.models.user import Role, User
from app.services.guardrails import check_guardrails
from sqlalchemy import insert


@pytest.mark.asyncio
async def test_guardrails_max_open_tickets(db_session):
    parent = User(phone=f"+91999{uuid.uuid4().hex[:7]}", role=Role.PARENT, school_id=1)
    db_session.add(parent)
    await db_session.flush()
    for i in range(3):
        t = Ticket(
            school_id=1,
            created_by_id=parent.id,
            category=TicketCategory.TRANSPORT,
            status=TicketStatus.PENDING,
        )
        db_session.add(t)
        await db_session.flush()
    await db_session.commit()
    err = await check_guardrails(db_session, parent, TicketCategory.TRANSPORT)
    assert err is not None
    assert "maximum number of open tickets" in err


@pytest.mark.asyncio
async def test_guardrails_cooldown(db_session):
    parent = User(phone=f"+91999{uuid.uuid4().hex[:7]}", role=Role.PARENT, school_id=1)
    db_session.add(parent)
    await db_session.flush()
    t = Ticket(
        school_id=1,
        created_by_id=parent.id,
        category=TicketCategory.TRANSPORT,
        status=TicketStatus.RESOLVED,
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(t)
    await db_session.commit()
    err = await check_guardrails(db_session, parent, TicketCategory.TRANSPORT)
    assert err is not None
    assert "wait" in err.lower()


@pytest.mark.asyncio
async def test_guardrails_allowed_when_under_limits(db_session):
    parent = User(phone=f"+91999{uuid.uuid4().hex[:7]}", role=Role.PARENT, school_id=1)
    db_session.add(parent)
    await db_session.commit()
    err = await check_guardrails(db_session, parent, TicketCategory.TRANSPORT)
    assert err is None


@pytest.mark.asyncio
async def test_guardrails_urgent_only_allowed_categories(db_session):
    parent = User(phone=f"+91999{uuid.uuid4().hex[:7]}", role=Role.PARENT, school_id=1)
    db_session.add(parent)
    await db_session.commit()
    err = await check_guardrails(db_session, parent, TicketCategory.OTHER, urgency=True)
    assert err is not None
    assert "Urgent" in err and "Transport" in err