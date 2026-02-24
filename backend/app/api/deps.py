# ABOUTME: FastAPI dependencies (DB session, auth, etc.).
# ABOUTME: get_db yields async session from app-state engine.

from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session_factory


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    engine = request.app.state.engine
    factory = get_session_factory(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
