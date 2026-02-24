# ABOUTME: Auth request/response schemas for OTP and tokens.

from pydantic import BaseModel, Field


class RequestOTPBody(BaseModel):
    phone: str = Field(..., min_length=10, max_length=20)


class VerifyOTPBody(BaseModel):
    phone: str = Field(..., min_length=10, max_length=20)
    code: str = Field(..., min_length=6, max_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str
