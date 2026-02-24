# ABOUTME: SQLAlchemy declarative base for all models.
# ABOUTME: All tables use this base for migrations and mapping.

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
