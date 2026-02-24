# ABOUTME: E2E test: parent creates ticket, staff resolves, parent marks satisfied.
# ABOUTME: Full flow without mocks; uses real DB and APIs.

import uuid

import pytest
from jose import jwt

from app.core.config import get_settings
from app.models.student import Student, parent_students
from app.models.ticket import TicketCategory
from app.models.user import Role, User
from sqlalchemy import insert


def _token(role: Role, user_id: int, school_id: int = 1) -> str:
    from datetime import datetime, timezone, timedelta
    return jwt.encode(
        {"sub": str(user_id), "role": role.value, "school_id": school_id, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)},
        get_settings().jwt_access_secret,
        algorithm="HS256",
    )


@pytest.mark.asyncio
async def test_e2e_parent_creates_staff_resolves_parent_satisfied(client, db_session):
    phone_p = f"+91999{uuid.uuid4().hex[:7]}"
    phone_t = f"+91998{uuid.uuid4().hex[:7]}"
    parent = User(phone=phone_p, role=Role.PARENT, school_id=1)
    teacher = User(phone=phone_t, role=Role.TEACHER, school_id=1)
    db_session.add(parent)
    db_session.add(teacher)
    await db_session.flush()
    student = Student(school_id=1, class_name="5", section="A")
    db_session.add(student)
    await db_session.flush()
    await db_session.execute(insert(parent_students).values(parent_id=parent.id, student_id=student.id))
    await db_session.commit()

    r1 = await client.post(
        "/tickets",
        headers={"Authorization": f"Bearer {_token(Role.PARENT, parent.id)}"},
        json={"student_ids": [student.id], "category": "academic_teaching", "title": "Homework query"},
    )
    assert r1.status_code == 200
    ticket_id = r1.json()["id"]

    r2 = await client.patch(
        f"/tickets/{ticket_id}/status",
        headers={"Authorization": f"Bearer {_token(Role.TEACHER, teacher.id)}"},
        json={"status": "resolved"},
    )
    assert r2.status_code == 200
    assert r2.json()["status"] == "resolved"

    r3 = await client.post(
        f"/tickets/{ticket_id}/satisfied",
        headers={"Authorization": f"Bearer {_token(Role.PARENT, parent.id)}"},
    )
    assert r3.status_code == 200

    r4 = await client.get(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {_token(Role.PARENT, parent.id)}"})
    assert r4.status_code == 200
    assert r4.json()["satisfied_at"] is not None
