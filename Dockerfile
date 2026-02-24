# ABOUTME: Production image for Syncdesk backend (FastAPI).
# ABOUTME: Uses UV for install and non-root user.

FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY backend/pyproject.toml backend/uv.lock* ./
COPY backend/app ./app
COPY backend/alembic.ini ./
COPY backend/alembic ./alembic
RUN uv sync --frozen --no-dev 2>/dev/null || uv sync --no-dev

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN chown -R nobody:nogroup /app

USER nobody

EXPOSE 8000

CMD ["sh", "-c", ".venv/bin/alembic upgrade head && .venv/bin/python -m app.seed && exec .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000"]
