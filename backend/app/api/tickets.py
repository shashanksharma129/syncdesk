# ABOUTME: Ticket CRUD, reply, and internal notes endpoints.
# ABOUTME: Parents see own tickets; staff see by school; internal notes hidden from parents.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_user, require_roles
from app.models.ticket import TicketCategory, TicketStatus
from app.models.user import Role, User
from app.schemas.ticket import InternalNoteIn, KnownIssueUpdate, MessageIn, MessageOut, ReopenIn, StatusUpdate, TicketCreate, TicketOut
from app.services.abuse_service import flag_abuse
from app.services.audit_service import log_audit
from app.services.guardrails import check_guardrails
from app.services.ticket_service import (
    add_internal_note,
    add_reply,
    create_ticket,
    get_internal_notes_count,
    get_ticket_for_user,
    get_ticket_messages,
    get_ticket_student_ids,
    get_parent_student_ids,
    list_tickets_for_user,
    mark_satisfied,
    request_reopen,
    set_ticket_known_issue,
    set_ticket_status,
)

router = APIRouter(prefix="/tickets", tags=["tickets"])


def _message_to_out(msg, is_staff_map: dict[int, bool]) -> MessageOut:
    return MessageOut(
        id=msg.id,
        ticket_id=msg.ticket_id,
        sender_id=msg.sender_id,
        body=msg.body,
        created_at=msg.created_at,
        is_staff=is_staff_map.get(msg.sender_id, False),
    )


async def _ticket_to_out(
    session: AsyncSession,
    ticket,
    current_user: User,
) -> TicketOut:
    student_ids = await get_ticket_student_ids(session, ticket.id)
    messages = await get_ticket_messages(session, ticket.id)
    sender_ids = list({m.sender_id for m in messages})
    is_staff_map = {}
    if sender_ids:
        result = await session.execute(select(User).where(User.id.in_(sender_ids)))
        for u in result.scalars().all():
            is_staff_map[u.id] = u.role != Role.PARENT
    internal_notes_count = None
    if current_user.role != Role.PARENT:
        internal_notes_count = await get_internal_notes_count(session, ticket.id)
    return TicketOut(
        id=ticket.id,
        school_id=ticket.school_id,
        created_by_id=ticket.created_by_id,
        category=ticket.category,
        status=ticket.status.value,
        urgency=ticket.urgency,
        assigned_to_id=ticket.assigned_to_id,
        title=ticket.title,
        description=ticket.description,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
        student_ids=student_ids,
        messages=[_message_to_out(m, is_staff_map) for m in messages],
        internal_notes_count=internal_notes_count,
        satisfied_at=getattr(ticket, "satisfied_at", None),
        transport_footer="No action required from parents." if ticket.category == TicketCategory.TRANSPORT else None,
        known_issue=getattr(ticket, "known_issue", False),
    )


@router.post("", response_model=TicketOut)
async def post_ticket(
    body: TicketCreate,
    current_user: User = Depends(require_roles(Role.PARENT)),
    db: AsyncSession = Depends(get_db),
):
    guardrail_error = await check_guardrails(db, current_user, body.category, body.urgency)
    if guardrail_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=guardrail_error)
    allowed_student_ids = await get_parent_student_ids(db, current_user.id)
    for sid in body.student_ids:
        if sid not in allowed_student_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All selected students must be linked to your account.",
            )
    ticket = await create_ticket(
        db,
        current_user,
        body.student_ids,
        body.category,
        body.title,
        body.description,
        body.urgency,
    )
    await db.flush()
    return await _ticket_to_out(db, ticket, current_user)


@router.get("", response_model=list[TicketOut])
async def list_tickets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    tickets = await list_tickets_for_user(db, current_user)
    return [await _ticket_to_out(db, t, current_user) for t in tickets]


@router.get("/{ticket_id}", response_model=TicketOut)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ticket = await get_ticket_for_user(db, ticket_id, current_user)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return await _ticket_to_out(db, ticket, current_user)


@router.post("/{ticket_id}/reply", response_model=TicketOut)
async def reply_ticket(
    ticket_id: int,
    body: MessageIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    msg = await add_reply(db, ticket_id, current_user, body.body)
    if not msg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    ticket = await get_ticket_for_user(db, ticket_id, current_user)
    return await _ticket_to_out(db, ticket, current_user)


@router.patch("/{ticket_id}/status", response_model=TicketOut)
async def update_ticket_status(
    ticket_id: int,
    body: StatusUpdate,
    current_user: User = Depends(require_roles(Role.DIRECTOR, Role.PRINCIPAL, Role.VICE_PRINCIPAL, Role.TEACHER, Role.OFFICE, Role.TRANSPORT)),
    db: AsyncSession = Depends(get_db),
):
    status_map = {"in_progress": TicketStatus.IN_PROGRESS, "resolved": TicketStatus.RESOLVED}
    if body.status not in status_map:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status.")
    ok = await set_ticket_status(db, ticket_id, current_user, status_map[body.status])
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found.")
    ticket = await get_ticket_for_user(db, ticket_id, current_user)
    return await _ticket_to_out(db, ticket, current_user)


@router.post("/{ticket_id}/reopen")
async def reopen_ticket(
    ticket_id: int,
    body: ReopenIn,
    current_user: User = Depends(require_roles(Role.PARENT)),
    db: AsyncSession = Depends(get_db),
):
    reopen = await request_reopen(db, ticket_id, current_user, body.reason)
    if not reopen:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket cannot be reopened. It may not be resolved, or you have reached the maximum reopen requests for this ticket.",
        )
    return {"id": reopen.id, "message": "Reopen request submitted."}


@router.post("/{ticket_id}/satisfied")
async def satisfied_ticket(
    ticket_id: int,
    current_user: User = Depends(require_roles(Role.PARENT)),
    db: AsyncSession = Depends(get_db),
):
    ok = await mark_satisfied(db, ticket_id, current_user)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ticket not found or not resolved.")
    return {"message": "Thank you for confirming."}


@router.patch("/{ticket_id}/known-issue")
async def update_known_issue(
    ticket_id: int,
    body: KnownIssueUpdate,
    current_user: User = Depends(require_roles(Role.TRANSPORT)),
    db: AsyncSession = Depends(get_db),
):
    ok = await set_ticket_known_issue(db, ticket_id, current_user, body.known_issue)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found.")
    ticket = await get_ticket_for_user(db, ticket_id, current_user)
    return await _ticket_to_out(db, ticket, current_user)


@router.post("/{ticket_id}/flag-abuse")
async def flag_ticket_abuse(
    ticket_id: int,
    current_user: User = Depends(require_roles(Role.DIRECTOR, Role.PRINCIPAL, Role.VICE_PRINCIPAL, Role.TEACHER, Role.OFFICE, Role.TRANSPORT)),
    db: AsyncSession = Depends(get_db),
):
    ticket = await flag_abuse(db, ticket_id, current_user)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found.")
    await log_audit(db, current_user.school_id, "ticket_abuse_flagged", current_user.id, "ticket", str(ticket_id), None)
    return {"message": "Ticket flagged for review. Director has been notified."}


@router.post("/{ticket_id}/internal-notes")
async def post_internal_note(
    ticket_id: int,
    body: InternalNoteIn,
    current_user: User = Depends(require_roles(Role.DIRECTOR, Role.PRINCIPAL, Role.VICE_PRINCIPAL, Role.TEACHER, Role.OFFICE, Role.TRANSPORT)),
    db: AsyncSession = Depends(get_db),
):
    note = await add_internal_note(db, ticket_id, current_user, body.body)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return {"id": note.id, "created_at": note.created_at}