# ABOUTME: FastAPI application entry and /health endpoint.
# ABOUTME: Mounts API router and configures CORS and lifespan.

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api import admin, announcements, auth, config, health, me, tickets
from app.core.config import get_settings
from app.core.db import get_engine
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    settings = get_settings()
    engine = get_engine(settings.database_url)
    app.state.engine = engine
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        raise RuntimeError(f"Database connectivity check failed: {e}") from e
    yield
    await engine.dispose()


app = FastAPI(
    title="School Communication & Helpdesk OS",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    from fastapi import HTTPException
    from fastapi.responses import JSONResponse
    if isinstance(exc, HTTPException):
        raise exc
    import logging
    logging.getLogger("syncdesk").exception("Unhandled error")
    return JSONResponse(status_code=500, content={"detail": "An error occurred. Please try again later."})

app.include_router(health.router, prefix="/health")
app.include_router(auth.router)
app.include_router(me.router)
app.include_router(tickets.router)
app.include_router(announcements.router)
app.include_router(admin.router)
app.include_router(config.router)


@app.get("/")
async def root():
    return {"service": "syncdesk-api", "docs": "/docs"}
