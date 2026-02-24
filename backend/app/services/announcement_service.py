# ABOUTME: List announcements for user (by targeting), create (staff), mark read.

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.announcement import Announcement, AnnouncementRead
from app.models.user import Role, User


async def list_announcements_for_user(session: AsyncSession, user: User) -> list[tuple[Announcement, bool]]:
    q = select(Announcement).where(Announcement.school_id == user.school_id).order_by(Announcement.created_at.desc())
    result = await session.execute(q)
    announcements = result.scalars().all()
    out = []
    for a in announcements:
        if user.role == Role.PARENT and a.target_audience == "staff":
            continue
        if user.role != Role.PARENT and a.target_audience == "parents":
            continue
        read_result = await session.execute(
            select(AnnouncementRead).where(
                AnnouncementRead.announcement_id == a.id,
                AnnouncementRead.user_id == user.id,
            )
        )
        read = read_result.scalar_one_or_none() is not None
        out.append((a, read))
    return out


async def create_announcement(
    session: AsyncSession,
    author: User,
    title: str,
    content: str,
    target_audience: str,
    target_grade: str | None,
    target_class: str | None,
) -> Announcement:
    a = Announcement(
        school_id=author.school_id,
        author_id=author.id,
        title=title,
        content=content,
        target_audience=target_audience,
        target_grade=target_grade,
        target_class=target_class,
    )
    session.add(a)
    await session.flush()
    return a


async def mark_announcement_read(session: AsyncSession, announcement_id: int, user_id: int) -> bool:
    r = await session.execute(select(Announcement).where(Announcement.id == announcement_id))
    if r.scalar_one_or_none() is None:
        return False
    existing = await session.execute(
        select(AnnouncementRead).where(
            AnnouncementRead.announcement_id == announcement_id,
            AnnouncementRead.user_id == user_id,
        )
    )
    if existing.scalar_one_or_none():
        return True
    session.add(AnnouncementRead(announcement_id=announcement_id, user_id=user_id))
    await session.flush()
    return True
