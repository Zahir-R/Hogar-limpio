from fastapi import APIRouter, Depends
from models.schemas import ServiceSchema, ServiceUpdateSchema
from services.service_service import ServiceService
from shared.auth import require_role

router = APIRouter(tags=["services"])
service_service = ServiceService()


@router.post("/api/servicios/registrar")
async def registrar_servicio(data: ServiceSchema, user: dict = Depends(require_role("personal_limpieza"))):
    return service_service.create(user.get("uid"), data)


@router.get("/api/servicios/mis-servicios")
async def listar_mis_servicios(user: dict = Depends(require_role("personal_limpieza"))):
    return service_service.list_mine(user.get("uid"))


@router.put("/api/servicios/{servicio_id}")
async def editar_servicio(servicio_id: str, data: ServiceUpdateSchema, user: dict = Depends(require_role("personal_limpieza"))):
    return service_service.update(servicio_id, user.get("uid"), data)


@router.delete("/api/servicios/{servicio_id}")
async def eliminar_servicio(servicio_id: str, user: dict = Depends(require_role("personal_limpieza"))):
    return service_service.delete(servicio_id, user.get("uid"))
