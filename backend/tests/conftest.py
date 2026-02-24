# ABOUTME: Pytest fixtures and test client for FastAPI.
# ABOUTME: Provides async client and DB session (rollback) for tests.

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import get_engine, get_session_factory
from app.main import app


@pytest.fixture
async def client():
    settings = get_settings()
    engine = get_engine(settings.database_url)
    app.state.engine = engine
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    await engine.dispose()


@pytest.fixture
async def db_session():
    """Provides an async DB session that rolls back after the test."""
    settings = get_settings()
    engine = get_engine(settings.database_url)
    factory = get_session_factory(engine)
    async with factory() as session:
        yield session
        await session.rollback()
    await engine.dispose()
