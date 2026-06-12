from fastapi import APIRouter, Depends
from models.schemas import UserUpdate
from services.user_service import UserService
from services.service_service import ServiceService
from shared.auth import require_role
from models.schemas import AdminValidationBody

router = APIRouter(tags=["admin"])
user_service = UserService()
service_service = ServiceService()


@router.get("/admin/users")
async def list_users(admin: dict = Depends(require_role("admin"))):
    return user_service.list_users()


@router.post("/admin/users/{uid}/update")
async def update_user(uid: str, data: UserUpdate, admin: dict = Depends(require_role("admin"))):
    return user_service.admin_update(uid, data)


@router.delete("/admin/users/{uid}")
async def delete_user(uid: str, admin: dict = Depends(require_role("admin"))):
    return user_service.admin_delete(uid)


@router.get("/api/admin/servicios/pendientes")
async def servicios_pendientes(admin: dict = Depends(require_role("admin"))):
    return service_service.list_pending()


@router.patch("/api/admin/servicios/{servicio_id}/validar")
async def validar_servicio(servicio_id: str, data: AdminValidationBody, admin: dict = Depends(require_role("admin"))):
    return service_service.validate(servicio_id, data.estado)
