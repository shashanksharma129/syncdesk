# ABOUTME: Admin-only endpoints: abuse list, restrict/block parent, metrics, export.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import require_roles
from app.models.announcement import Announcement, AnnouncementRead
from app.models.ticket import Ticket, TicketReopen, TicketStatus
from app.models.user import Role, User
from app.services.abuse_service import (
    block_parent_ticket_creation,
    list_abuse_flagged,
    restrict_parent_to_admin,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/abuse-flagged")
async def get_abuse_flagged(
    current_user: User = Depends(require_roles(Role.DIRECTOR)),
    db: AsyncSession = Depends(get_db),
):
    tickets = await list_abuse_flagged(db, current_user.school_id)
    return [{"id": t.id, "created_by_id": t.created_by_id, "abuse_flagged_at": str(t.abuse_flagged_at)} for t in tickets]


@router.post("/users/{user_id}/restrict")
async def restrict_user(
    user_id: int,
    current_user: User = Depends(require_roles(Role.DIRECTOR)),
    db: AsyncSession = Depends(get_db),
):
    user = await restrict_parent_to_admin(db, user_id, current_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return {"message": "Parent restricted.", "until": str(user.restricted_to_admin_until)}


@router.post("/users/{user_id}/block-tickets")
async def block_user_tickets(
    user_id: int,
    current_user: User = Depends(require_roles(Role.DIRECTOR)),
    db: AsyncSession = Depends(get_db),
):
    user = await block_parent_ticket_creation(db, user_id, current_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return {"message": "Ticket creation blocked.", "until": str(user.ticket_creation_blocked_until)}


@router.get("/metrics")
async def get_metrics(
    current_user: User = Depends(require_roles(Role.DIRECTOR, Role.PRINCIPAL)),
    db: AsyncSession = Depends(get_db),
):
    q = select(
        func.count(Ticket.id).label("total"),
        func.count(Ticket.id).filter(Ticket.status == TicketStatus.RESOLVED).label("resolved"),
    ).where(Ticket.school_id == current_user.school_id, Ticket.deleted_at.is_(None))
    r = (await db.execute(q)).one()
    reopen_count = (await db.execute(select(func.count(TicketReopen.id)))).scalar() or 0
    ann_q = select(func.count(AnnouncementRead.id)).join(Announcement).where(Announcement.school_id == current_user.school_id)
    ann_reads = (await db.execute(ann_q)).scalar() or 0
    return {
        "tickets_total": r.total,
        "tickets_resolved": r.resolved,
        "reopen_requests_total": reopen_count,
        "announcement_reads_total": ann_reads,
    }


@router.get("/export/tickets")
async def export_tickets(
    current_user: User = Depends(require_roles(Role.DIRECTOR)),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ticket).where(
            Ticket.school_id == current_user.school_id,
            Ticket.deleted_at.is_(None),
        ).order_by(Ticket.created_at.desc()).limit(1000)
    )
    tickets = result.scalars().all()
    return {
        "watermark": f"Syncdesk export | School ID {current_user.school_id} | For official use only",
        "tickets": [{"id": t.id, "category": t.category.value, "status": t.status.value, "created_at": str(t.created_at)} for t in tickets],
    }
