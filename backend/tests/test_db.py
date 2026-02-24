# ABOUTME: Tests for database connectivity and session.
# ABOUTME: Ensures async engine and session work against test DB.

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import get_engine, get_session


@pytest.mark.asyncio
async def test_db_connection():
    settings = get_settings()
    engine = get_engine(settings.database_url)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.scalar_one()
        assert row == 1
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_session_returns_session():
    settings = get_settings()
    engine = get_engine(settings.database_url)
    try:
        async for session in get_session(engine):
            assert session is not None
            assert isinstance(session, AsyncSession)
            break
    finally:
        await engine.dispose()
