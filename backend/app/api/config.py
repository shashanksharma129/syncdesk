# ABOUTME: Config endpoints: office hours and banner text for off-hours.

from datetime import datetime

from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.core.config import get_settings
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/office-hours")
async def office_hours(
    current_user: User = Depends(get_current_user),
):
    settings = get_settings()
    try:
        start = datetime.strptime(settings.office_hours_start, "%H:%M").time()
        end = datetime.strptime(settings.office_hours_end, "%H:%M").time()
    except ValueError:
        start = datetime.strptime("08:00", "%H:%M").time()
        end = datetime.strptime("17:00", "%H:%M").time()
    now = datetime.utcnow().time()
    in_hours = start <= now <= end if start <= end else (now >= start or now <= end)
    banner = None
    if not in_hours:
        banner = f"School office hours are {settings.office_hours_start}–{settings.office_hours_end}. Requests will be addressed next working day."
    return {"in_office_hours": in_hours, "banner": banner, "start": settings.office_hours_start, "end": settings.office_hours_end}
