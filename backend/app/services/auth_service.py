# ABOUTME: Auth business logic: request OTP, verify OTP, issue JWT.
# ABOUTME: Creates parent user on first verify; marks OTP used.

import logging
from datetime import datetime, timezone, timedelta

from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.user import OTP, Role, User
from app.services.otp_service import (
    generate_otp_code,
    hash_otp,
    otp_expires_at,
    stub_deliver_otp,
    verify_otp,
)

logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(user_id: int, role: Role, school_id: int) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "role": role.value, "school_id": school_id, "exp": expire}
    return jwt.encode(payload, settings.jwt_access_secret, algorithm="HS256")


async def request_otp(session: AsyncSession, phone: str) -> None:
    code = generate_otp_code()
    hashed = hash_otp(code)
    expires = otp_expires_at()
    otp = OTP(phone=phone, hashed_code=hashed, expires_at=expires, used=False)
    session.add(otp)
    await session.flush()
    stub_deliver_otp(phone, code)


async def verify_otp_and_issue_token(
    session: AsyncSession, phone: str, code: str
) -> tuple[User, str] | None:
    result = await session.execute(
        select(OTP).where(OTP.phone == phone).order_by(OTP.id.desc()).limit(1)
    )
    otp_row = result.scalar_one_or_none()
    if not otp_row:
        return None
    if otp_row.used:
        return None
    exp = otp_row.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if exp < datetime.now(timezone.utc):
        return None
    settings = get_settings()
    stub_ok = (
        settings.app_env == "development"
        and settings.stub_otp_code
        and code.strip() == settings.stub_otp_code
    )
    stub_staff_ok = (
        settings.app_env == "development"
        and settings.stub_otp_staff_code
        and code.strip() == settings.stub_otp_staff_code
    )
    if not stub_ok and not stub_staff_ok and not verify_otp(code, otp_row.hashed_code):
        return None
    otp_row.used = True
    await session.flush()

    result = await session.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    if not user:
        role = Role.TEACHER if stub_staff_ok else Role.PARENT
        user = User(phone=phone, role=role, school_id=settings.default_school_id)
        session.add(user)
        await session.flush()
    else:
        if stub_staff_ok and user.role == Role.PARENT:
            user.role = Role.TEACHER
            await session.flush()
        elif stub_ok and user.role != Role.PARENT:
            user.role = Role.PARENT
            await session.flush()
    token = create_access_token(user.id, user.role, user.school_id)
    return (user, token)
