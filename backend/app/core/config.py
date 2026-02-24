# ABOUTME: Pydantic settings for env-based configuration.
# ABOUTME: Loads DATABASE_URL, JWT secrets, and optional integrations.

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    log_level: str = "INFO"
    stub_otp_code: str = ""
    """If set (e.g. 123456), in development this code is accepted for any phone that requested OTP."""
    stub_otp_staff_code: str = ""
    """If set (e.g. 654321), in development this code logs in as staff (teacher) for that phone."""

    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/syncdesk"
    jwt_access_secret: str = ""
    jwt_refresh_secret: str = ""

    default_school_id: int = 1
    office_hours_start: str = "08:00"
    office_hours_end: str = "17:00"
    office_hours_timezone: str = "Asia/Kolkata"


def get_settings() -> Settings:
    return Settings()
