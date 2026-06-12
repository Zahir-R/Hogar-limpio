from fastapi import APIRouter, Depends
from models.schemas import AvailabilityTemplate, DateOverride
from services.availability_service import AvailabilityService
from shared.auth import get_current_user, require_role

router = APIRouter(tags=["availability"])
availability_service = AvailabilityService()


@router.get("/api/availability/{worker_uid}")
async def get_availability(worker_uid: str, current_user: dict = Depends(get_current_user)):
    return availability_service.get(worker_uid)


@router.put("/api/availability")
async def save_availability_template(data: AvailabilityTemplate, current_user: dict = Depends(require_role("personal_limpieza"))):
    return availability_service.save_template(current_user["uid"], data)


@router.post("/api/availability/toggle")
async def toggle_availability_override(data: DateOverride, current_user: dict = Depends(require_role("personal_limpieza"))):
    return availability_service.toggle_override(current_user["uid"], data)
