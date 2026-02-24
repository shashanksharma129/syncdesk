# ABOUTME: Tests for ticket APIs: create, list, get, reply, internal notes, visibility.
# ABOUTME: Parent creates ticket; staff reply sets In Progress; internal notes staff-only.

import uuid

import pytest
from jose import jwt

from app.core.config import get_settings
from app.models.student import Student, parent_students
from app.models.ticket import TicketCategory
from app.models.user import Role, User
from sqlalchemy import insert


def _make_token(role: Role, user_id: int, school_id: int = 1) -> str:
    from datetime import datetime, timezone, timedelta
    settings = get_settings()
    exp = datetime.now(timezone.utc) + timedelta(minutes=15)
    return jwt.encode(
        {"sub": str(user_id), "role": role.value, "school_id": school_id, "exp": exp},
        settings.jwt_access_secret,
        algorithm="HS256",
    )


@pytest.mark.asyncio
async def test_parent_creates_ticket(client, db_session):
    phone = f"+91999{uuid.uuid4().hex[:7]}"
    parent = User(phone=phone, role=Role.PARENT, school_id=1)
    db_session.add(parent)
    await db_session.flush()
    student = Student(school_id=1, class_name="5", section="A")
    db_session.add(student)
    await db_session.flush()
    await db_session.execute(insert(parent_students).values(parent_id=parent.id, student_id=student.id))
    await db_session.commit()
    token = _make_token(Role.PARENT, parent.id)
    r = await client.post(
        "/tickets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "student_ids": [student.id],
            "category": "transport",
            "title": "Bus delay",
            "urgency": False,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["category"] == "transport"
    assert data["status"] == "pending"
    assert data["student_ids"] == [student.id]
    assert data["title"] == "Bus delay"


@pytest.mark.asyncio
async def test_parent_lists_own_tickets(client, db_session):
    phone = f"+91999{uuid.uuid4().hex[:7]}"
    parent = User(phone=phone, role=Role.PARENT, school_id=1)
    db_session.add(parent)
    await db_session.flush()
    student = Student(school_id=1, class_name="6", section="B")
    db_session.add(student)
    await db_session.flush()
    await db_session.execute(insert(parent_students).values(parent_id=parent.id, student_id=student.id))
    from app.models.ticket import Ticket, TicketStatus, ticket_students
    from sqlalchemy import insert as sql_insert
    ticket = Ticket(school_id=1, created_by_id=parent.id, category=TicketCategory.TRANSPORT, status=TicketStatus.PENDING)
    db_session.add(ticket)
    await db_session.flush()
    await db_session.execute(sql_insert(ticket_students).values(ticket_id=ticket.id, student_id=student.id))
    await db_session.commit()
    token = _make_token(Role.PARENT, parent.id)
    r = await client.get("/tickets", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 1
    assert data[0]["created_by_id"] == parent.id


@pytest.mark.asyncio
async def test_staff_reply_sets_in_progress(client, db_session):
    phone = f"+91999{uuid.uuid4().hex[:7]}"
    parent = User(phone=phone, role=Role.PARENT, school_id=1)
    db_session.add(parent)
    await db_session.flush()
    teacher = User(phone=f"+91998{uuid.uuid4().hex[:7]}", role=Role.TEACHER, school_id=1)
    db_session.add(teacher)
    await db_session.flush()
    from app.models.ticket import Ticket, TicketStatus, ticket_students
    from sqlalchemy import insert as sql_insert
    ticket = Ticket(school_id=1, created_by_id=parent.id, category=TicketCategory.ACADEMIC_TEACHING, status=TicketStatus.PENDING)
    db_session.add(ticket)
    await db_session.flush()
    await db_session.commit()
    token = _make_token(Role.TEACHER, teacher.id)
    r = await client.post(
        f"/tickets/{ticket.id}/reply",
        headers={"Authorization": f"Bearer {token}"},
        json={"body": "We will look into it."},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "in_progress"
    assert len(r.json()["messages"]) == 1
    assert r.json()["messages"][0]["body"] == "We will look into it."
    assert r.json()["messages"][0]["is_staff"] is True


@pytest.mark.asyncio
async def test_internal_notes_not_in_parent_response(client, db_session):
    phone = f"+91999{uuid.uuid4().hex[:7]}"
    parent = User(phone=phone, role=Role.PARENT, school_id=1)
    db_session.add(parent)
    await db_session.flush()
    vp = User(phone=f"+91997{uuid.uuid4().hex[:7]}", role=Role.VICE_PRINCIPAL, school_id=1)
    db_session.add(vp)
    await db_session.flush()
    from app.models.ticket import Ticket, TicketStatus
    ticket = Ticket(school_id=1, created_by_id=parent.id, category=TicketCategory.DISCIPLINE, status=TicketStatus.PENDING)
    db_session.add(ticket)
    await db_session.flush()
    await db_session.commit()
    vp_token = _make_token(Role.VICE_PRINCIPAL, vp.id)
    r_note = await client.post(
        f"/tickets/{ticket.id}/internal-notes",
        headers={"Authorization": f"Bearer {vp_token}"},
        json={"body": "Internal note here"},
    )
    assert r_note.status_code == 200
    parent_token = _make_token(Role.PARENT, parent.id)
    r_get = await client.get(f"/tickets/{ticket.id}", headers={"Authorization": f"Bearer {parent_token}"})
    assert r_get.status_code == 200
    assert "internal_notes_count" not in r_get.json() or r_get.json().get("internal_notes_count") is None
    r_staff = await client.get(f"/tickets/{ticket.id}", headers={"Authorization": f"Bearer {vp_token}"})
    assert r_staff.status_code == 200
    assert r_staff.json().get("internal_notes_count") == 1