# ABOUTME: Tests for announcements: list (targeted), create (staff), mark read.

import uuid

import pytest
from jose import jwt

from app.core.config import get_settings
from app.models.announcement import Announcement
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
async def test_staff_creates_announcement(client, db_session):
    vp = User(phone=f"+91999{uuid.uuid4().hex[:7]}", role=Role.VICE_PRINCIPAL, school_id=1)
    db_session.add(vp)
    await db_session.commit()
    r = await client.post(
        "/announcements",
        headers={"Authorization": f"Bearer {_make_token(Role.VICE_PRINCIPAL, vp.id)}"},
        json={"title": "Holiday", "content": "School closed tomorrow.", "target_audience": "both"},
    )
    assert r.status_code == 200
    assert r.json()["title"] == "Holiday"
    assert r.json()["target_audience"] == "both"


@pytest.mark.asyncio
async def test_parent_lists_announcements(client, db_session):
    parent = User(phone=f"+91999{uuid.uuid4().hex[:7]}", role=Role.PARENT, school_id=1)
    db_session.add(parent)
    await db_session.flush()
    a = Announcement(school_id=1, author_id=parent.id, title="Test", content="Body", target_audience="parents")
    db_session.add(a)
    await db_session.commit()
    r = await client.get("/announcements", headers={"Authorization": f"Bearer {_make_token(Role.PARENT, parent.id)}"})
    assert r.status_code == 200
    assert len(r.json()) >= 1
    assert r.json()[0]["title"] == "Test"