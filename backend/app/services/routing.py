# ABOUTME: Category-to-role routing for tickets (spec: which role handles which category).
# ABOUTME: Used for default assignee suggestion and filtering.

from app.models.ticket import TicketCategory
from app.models.user import Role

CATEGORY_TO_ROLE: dict[TicketCategory, Role] = {
    TicketCategory.ACADEMIC_TEACHING: Role.TEACHER,
    TicketCategory.ACADEMIC_EXAM_POLICY: Role.VICE_PRINCIPAL,
    TicketCategory.DISCIPLINE: Role.VICE_PRINCIPAL,
    TicketCategory.ATTENDANCE_LEAVE: Role.TEACHER,
    TicketCategory.FEE_ACCOUNTS: Role.PRINCIPAL,
    TicketCategory.TRANSPORT: Role.TRANSPORT,
    TicketCategory.HEALTH_SAFETY: Role.VICE_PRINCIPAL,
    TicketCategory.CLEANLINESS_INFRA: Role.OFFICE,
    TicketCategory.DOCUMENTS: Role.OFFICE,
    TicketCategory.OTHER: Role.PRINCIPAL,
}


def get_role_for_category(category: TicketCategory) -> Role:
    return CATEGORY_TO_ROLE.get(category, Role.PRINCIPAL)
