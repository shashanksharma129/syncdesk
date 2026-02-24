# ABOUTME: Tests for role enforcement: 401 without token, 200 with valid token.
# ABOUTME: Uses GET /me to verify auth and role.

from datetime import datetime, timezone, timedelta

import pytest
from jose import jwt

from app.core.config import get_settings
from app.models.user import Role


def _make_token(role: Role = Role.PARENT, user_id: int = 1, school_id: int = 1) -> str:
    settings = get_settings()
    exp = datetime.now(timezone.utc) + timedelta(minutes=15)
    return jwt.encode(
        {"sub": str(user_id), "role": role.value, "school_id": school_id, "exp": exp},
        settings.jwt_access_secret,
        algorithm="HS256",
    )


@pytest.mark.asyncio
async def test_me_returns_401_without_token(client):
    r = await client.get("/me")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_me_returns_200_with_valid_token(client, db_session):
    import uuid
    from app.models.user import User

    phone = f"+91999{uuid.uuid4().hex[:7]}"
    user = User(phone=phone, role=Role.PARENT, school_id=1)
    db_session.add(user)
    await db_session.commit()
    token = _make_token(role=Role.PARENT, user_id=user.id)
    r = await client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["role"] == "parent"
    assert r.json()["phone"] == phone
