from fastapi import HTTPException
from repositories.user_repo import UserRepository
from repositories.service_repo import ServiceRepository


class WorkerService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.service_repo = ServiceRepository()

    def list(self, zona, current_user):
        role = current_user.get("role")
        if role not in ("cliente", "admin"):
            raise HTTPException(status_code=403, detail="Only clients and admins can browse workers")

        workers = self.user_repo.list_by_role("personal_limpieza", zona)
        for worker in workers:
            servicios = self.service_repo.list_approved_by_ofertante(worker["uid"])
            worker["servicios"] = servicios
        return workers

    def get_profile(self, uid):
        data = self.user_repo.get(uid)
        if not data:
            raise HTTPException(status_code=404, detail="Worker not found")
        if data.get("role") != "personal_limpieza":
            raise HTTPException(status_code=400, detail="User is not a worker")
        servicios = self.service_repo.list_approved_by_ofertante(uid)
        data["servicios"] = servicios
        return data
