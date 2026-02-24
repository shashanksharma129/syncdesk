# ABOUTME: Seed script for local/dev: parent, staff, students, tickets, announcements.
# ABOUTME: Idempotent: skips if seed data already present. Run after migrations.

import asyncio
import logging
import os
import sys

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import get_engine, get_session_factory
from app.models.announcement import Announcement
from app.models.student import Student, parent_students
from app.models.ticket import (
    Ticket,
    TicketCategory,
    TicketMessage,
    TicketStatus,
    ticket_students,
)
from app.models.user import Role, User

logger = logging.getLogger(__name__)

SEED_PARENT_PHONE = "+15550000001"
SEED_STAFF_PHONE = "+15550000002"
DEFAULT_SCHOOL_ID = 1


async def seed(session: AsyncSession) -> None:
    result = await session.execute(select(User).where(User.phone == SEED_PARENT_PHONE))
    if result.scalar_one_or_none() is not None:
        logger.info("Seed data already present; skipping.")
        return

    parent = User(
        phone=SEED_PARENT_PHONE,
        role=Role.PARENT,
        school_id=DEFAULT_SCHOOL_ID,
        name="Parent Demo",
        email="parent@example.com",
    )
    session.add(parent)
    await session.flush()

    staff = User(
        phone=SEED_STAFF_PHONE,
        role=Role.TEACHER,
        school_id=DEFAULT_SCHOOL_ID,
        name="Teacher Demo",
        email="teacher@example.com",
    )
    session.add(staff)
    await session.flush()

    s1 = Student(school_id=DEFAULT_SCHOOL_ID, class_name="5", section="A")
    s2 = Student(school_id=DEFAULT_SCHOOL_ID, class_name="3", section="B")
    session.add_all([s1, s2])
    await session.flush()

    await session.execute(insert(parent_students).values(parent_id=parent.id, student_id=s1.id))
    await session.execute(insert(parent_students).values(parent_id=parent.id, student_id=s2.id))
    await session.flush()

    t1 = Ticket(
        school_id=DEFAULT_SCHOOL_ID,
        created_by_id=parent.id,
        category=TicketCategory.TRANSPORT,
        status=TicketStatus.IN_PROGRESS,
        urgency=False,
        title="Bus delay on Route 12",
        description="Bus was 20 min late this morning.",
        assigned_to_id=staff.id,
    )
    t2 = Ticket(
        school_id=DEFAULT_SCHOOL_ID,
        created_by_id=parent.id,
        category=TicketCategory.ACADEMIC_TEACHING,
        status=TicketStatus.RESOLVED,
        urgency=False,
        title="Question about homework",
        description="Where can we find the reading list?",
        assigned_to_id=staff.id,
    )
    t3 = Ticket(
        school_id=DEFAULT_SCHOOL_ID,
        created_by_id=parent.id,
        category=TicketCategory.HEALTH_SAFETY,
        status=TicketStatus.PENDING,
        urgency=True,
        title="Allergy update",
        description="Child A has a new nut allergy. Please update records.",
    )
    session.add_all([t1, t2, t3])
    await session.flush()

    for ticket_id, student_ids in [(t1.id, [s1.id]), (t2.id, [s2.id]), (t3.id, [s1.id, s2.id])]:
        for sid in student_ids:
            await session.execute(insert(ticket_students).values(ticket_id=ticket_id, student_id=sid))
    await session.flush()

    m1 = TicketMessage(ticket_id=t1.id, sender_id=parent.id, body="Bus was 20 min late this morning.")
    m2 = TicketMessage(ticket_id=t1.id, sender_id=staff.id, body="We have noted this and will inform the driver.")
    m3 = TicketMessage(ticket_id=t2.id, sender_id=parent.id, body="Where can we find the reading list?")
    m4 = TicketMessage(ticket_id=t2.id, sender_id=staff.id, body="It is on the class portal under Resources.")
    m5 = TicketMessage(ticket_id=t3.id, sender_id=parent.id, body="Child A has a new nut allergy. Please update records.")
    session.add_all([m1, m2, m3, m4, m5])
    await session.flush()

    a1 = Announcement(
        school_id=DEFAULT_SCHOOL_ID,
        author_id=staff.id,
        title="School closed Monday",
        content="The school will be closed on Monday for a staff development day.",
        target_audience="both",
    )
    a2 = Announcement(
        school_id=DEFAULT_SCHOOL_ID,
        author_id=staff.id,
        title="Transport update",
        content="New pickup times for Route 5 from next week.",
        target_audience="parents",
    )
    session.add_all([a1, a2])
    await session.flush()

    logger.info("Seed completed: parent %s, staff %s, 2 students, 3 tickets, 2 announcements.", SEED_PARENT_PHONE, SEED_STAFF_PHONE)


async def run_seed() -> None:
    settings = get_settings()
    url = settings.database_url
    if not url or url.startswith("sqlite"):
        logger.warning("No DATABASE_URL or sqlite; skipping seed.")
        return
    engine = get_engine(url)
    factory = get_session_factory(engine)
    async with factory() as session:
        try:
            await seed(session)
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await engine.dispose()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    asyncio.run(run_seed())


if __name__ == "__main__":
    main()
    sys.exit(0)
