# ABOUTME: Announcements: list (targeted), create (staff), mark read.
# ABOUTME: One-way; no replies.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_user, require_roles
from app.models.user import Role, User
from app.schemas.announcement import AnnouncementCreate, AnnouncementOut
from app.services.announcement_service import (
    create_announcement,
    list_announcements_for_user,
    mark_announcement_read,
)

router = APIRouter(prefix="/announcements", tags=["announcements"])


@router.get("", response_model=list[AnnouncementOut])
async def list_announcements(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    pairs = await list_announcements_for_user(db, current_user)
    return [
        AnnouncementOut(
            id=a.id,
            school_id=a.school_id,
            author_id=a.author_id,
            title=a.title,
            content=a.content,
            target_audience=a.target_audience,
            target_grade=a.target_grade,
            target_class=a.target_class,
            created_at=a.created_at,
            read=read,
        )
        for a, read in pairs
    ]


@router.post("", response_model=AnnouncementOut)
async def post_announcement(
    body: AnnouncementCreate,
    current_user: User = Depends(require_roles(Role.DIRECTOR, Role.PRINCIPAL, Role.VICE_PRINCIPAL)),
    db: AsyncSession = Depends(get_db),
):
    a = await create_announcement(
        db, current_user,
        body.title, body.content,
        body.target_audience, body.target_grade, body.target_class,
    )
    return AnnouncementOut(
        id=a.id,
        school_id=a.school_id,
        author_id=a.author_id,
        title=a.title,
        content=a.content,
        target_audience=a.target_audience,
        target_grade=a.target_grade,
        target_class=a.target_class,
        created_at=a.created_at,
        read=False,
    )


@router.post("/{announcement_id}/read")
async def read_announcement(
    announcement_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ok = await mark_announcement_read(db, announcement_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found.")
    return {"message": "Marked as read."}
