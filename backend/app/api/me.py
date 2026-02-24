# ABOUTME: Current user (me) endpoints; used for auth and role testing.
# ABOUTME: GET /me and GET /me/students.

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.security import get_current_user
from app.models.student import Student, parent_students
from app.models.user import Role, User
from app.schemas.student import StudentOut, student_to_out

router = APIRouter(prefix="/me", tags=["me"])


@router.get("")
async def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "phone": user.phone, "role": user.role.value, "school_id": user.school_id}


@router.get("/students", response_model=list[StudentOut])
async def my_students(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if user.role != Role.PARENT:
        return []
    result = await db.execute(
        select(Student)
        .join(parent_students, parent_students.c.student_id == Student.id)
        .where(
            parent_students.c.parent_id == user.id,
            Student.school_id == user.school_id,
        )
    )
    students = result.scalars().all()
    return [student_to_out(s) for s in students]
