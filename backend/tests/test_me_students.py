# ABOUTME: Tests for GET /me/students: parent sees linked students, others get empty.

import uuid

import pytest
from jose import jwt

from app.core.config import get_settings
from app.models.student import Student, parent_students
from app.models.user import Role, User


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
async def test_me_students_parent_empty_returns_empty_list(client, db_session):
    phone = f"+91999{uuid.uuid4().hex[:7]}"
    user = User(phone=phone, role=Role.PARENT, school_id=1)
    db_session.add(user)
    await db_session.commit()
    token = _make_token(Role.PARENT, user.id)
    r = await client.get("/me/students", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_me_students_parent_with_linked_student_returns_student(client, db_session):
    phone = f"+91999{uuid.uuid4().hex[:7]}"
    user = User(phone=phone, role=Role.PARENT, school_id=1)
    db_session.add(user)
    await db_session.flush()
    student = Student(school_id=1, class_name="5", section="A")
    db_session.add(student)
    await db_session.flush()
    from sqlalchemy import insert
    await db_session.execute(insert(parent_students).values(parent_id=user.id, student_id=student.id))
    await db_session.commit()
    token = _make_token(Role.PARENT, user.id)
    r = await client.get("/me/students", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["class_name"] == "5"
    assert data[0]["section"] == "A"
    assert data[0]["school_id"] == 1
