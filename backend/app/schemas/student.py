# ABOUTME: Student response schemas for /me/students.

from pydantic import BaseModel, ConfigDict


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    school_id: int
    class_name: str
    section: str


def student_to_out(s) -> StudentOut:
    return StudentOut(
        id=s.id,
        school_id=s.school_id,
        class_name=s.class_name,
        section=s.section,
    )
