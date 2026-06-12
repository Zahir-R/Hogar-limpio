from fastapi import APIRouter, Depends
from shared.auth import require_role

router = APIRouter(tags=["cleaner"])


@router.get("/api/cleaner/jobs")
async def get_cleaner_jobs(user: dict = Depends(require_role("personal_limpieza"))):
    return [
        {
            "id": "job_101",
            "hora": "09:00",
            "tipo": "Limpieza Profunda Residencial",
            "direccion": "Calle de la Luna, 45. Edificio Ámbar, 4B",
            "cliente": "Elena Rodriguez",
            "estado": "en_curso"
        }
    ]


@router.post("/api/cleaner/complete/{job_id}")
async def complete_job(job_id: str, user: dict = Depends(require_role("personal_limpieza"))):
    return {"status": "success", "message": f"Trabajo {job_id} finalizado"}
