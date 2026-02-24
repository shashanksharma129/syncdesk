# ABOUTME: Auth routes: request OTP and verify OTP (issue JWT).
# ABOUTME: Enforces 5-min expiry and single-use OTP.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.auth import MessageResponse, RequestOTPBody, TokenResponse, VerifyOTPBody
from app.services.auth_service import request_otp, verify_otp_and_issue_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/request-otp", response_model=MessageResponse)
async def request_otp_endpoint(body: RequestOTPBody, db: AsyncSession = Depends(get_db)):
    await request_otp(db, body.phone)
    return MessageResponse(message="OTP sent")


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp_endpoint(body: VerifyOTPBody, db: AsyncSession = Depends(get_db)):
    result = await verify_otp_and_issue_token(db, body.phone, body.code)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    _user, token = result
    return TokenResponse(access_token=token)
