# ABOUTME: OTP generation, hashing, and verification.
# ABOUTME: 6-digit code, 5-minute expiry, single-use.

import hashlib
import logging
import secrets
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

OTP_EXPIRY_MINUTES = 5
OTP_LENGTH = 6
OTP_HASH_SALT = b"syncdesk-otp-v1"


def generate_otp_code() -> str:
    return "".join(secrets.choice("0123456789") for _ in range(OTP_LENGTH))


def hash_otp(code: str) -> str:
    h = hashlib.sha256(OTP_HASH_SALT + code.encode()).hexdigest()
    return h


def verify_otp(plain: str, hashed: str) -> bool:
    return hashlib.sha256(OTP_HASH_SALT + plain.encode()).hexdigest() == hashed


def otp_expires_at() -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES)


def stub_deliver_otp(phone: str, code: str) -> None:
    logger.info("OTP delivery (stub): phone=%s code=%s", phone, code)
