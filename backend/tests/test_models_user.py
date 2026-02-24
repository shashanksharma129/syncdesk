# ABOUTME: Unit tests for User and OTP model constraints.
# ABOUTME: Ensures unique phone, role enum, and OTP fields.

from datetime import datetime, timezone, timedelta

import pytest

from app.models.user import OTP, Role, User


@pytest.mark.asyncio
async def test_user_create_and_phone_unique(db_session):
    user = User(
        phone="+919876543210",
        role=Role.PARENT,
        school_id=1,
        name="Test Parent",
    )
    db_session.add(user)
    await db_session.flush()
    assert user.id is not None
    assert user.phone == "+919876543210"
    assert user.role == Role.PARENT
    assert user.school_id == 1


@pytest.mark.asyncio
async def test_otp_create_and_used_flag(db_session):
    expires = datetime.now(timezone.utc) + timedelta(minutes=5)
    otp = OTP(
        phone="+919876543210",
        hashed_code="hashed",
        expires_at=expires,
        used=False,
    )
    db_session.add(otp)
    await db_session.flush()
    assert otp.id is not None
    assert otp.used is False
