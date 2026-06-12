from fastapi import APIRouter, Depends
from models.schemas import ZoneCreate, ZoneUpdate
from services.zone_service import ZoneService
from shared.auth import require_role

router = APIRouter(tags=["zones"])
zone_service = ZoneService()


@router.get("/api/zonas")
async def list_active_zonas():
    return zone_service.list_active()


@router.get("/api/admin/zonas")
async def list_all_zonas(admin: dict = Depends(require_role("admin"))):
    return zone_service.list_all()


@router.post("/api/admin/zonas")
async def create_zona(data: ZoneCreate, admin: dict = Depends(require_role("admin"))):
    return zone_service.create(data)


@router.put("/api/admin/zonas/{zona_id}")
async def update_zona(zona_id: str, data: ZoneUpdate, admin: dict = Depends(require_role("admin"))):
    return zone_service.update(zona_id, data)


@router.delete("/api/admin/zonas/{zona_id}")
async def soft_delete_zona(zona_id: str, admin: dict = Depends(require_role("admin"))):
    return zone_service.soft_delete(zona_id)
