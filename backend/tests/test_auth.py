# ABOUTME: Tests for OTP auth: invalid OTP, expired OTP, successful login.
# ABOUTME: Uses real DB and stub OTP delivery.

from datetime import datetime, timezone, timedelta

import pytest

from app.models.user import OTP
from app.services.otp_service import hash_otp, otp_expires_at


@pytest.mark.asyncio
async def test_request_otp_returns_200(client):
    r = await client.post("/auth/request-otp", json={"phone": "+919999000011"})
    assert r.status_code == 200
    assert r.json()["message"] == "OTP sent"


@pytest.mark.asyncio
async def test_verify_otp_invalid_returns_401(client):
    r = await client.post(
        "/auth/verify-otp",
        json={"phone": "+919999000022", "code": "000000"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_verify_otp_expired_returns_401(client, db_session):
    expired = datetime.now(timezone.utc) - timedelta(minutes=10)
    otp = OTP(
        phone="+919999000033",
        hashed_code=hash_otp("123456"),
        expires_at=expired,
        used=False,
    )
    db_session.add(otp)
    await db_session.commit()
    r = await client.post(
        "/auth/verify-otp",
        json={"phone": "+919999000033", "code": "123456"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_verify_otp_success_returns_token(client, db_session):
    expires = otp_expires_at()
    otp = OTP(
        phone="+919999000044",
        hashed_code=hash_otp("654321"),
        expires_at=expires,
        used=False,
    )
    db_session.add(otp)
    await db_session.commit()
    r = await client.post(
        "/auth/verify-otp",
        json={"phone": "+919999000044", "code": "654321"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0
