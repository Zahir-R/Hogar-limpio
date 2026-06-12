from fastapi import HTTPException
from repositories.zone_repo import ZoneRepository


class ZoneService:
    def __init__(self):
        self.repo = ZoneRepository()

    def list_active(self):
        return self.repo.list_active()

    def list_all(self):
        return self.repo.list_all()

    def create(self, data):
        zone_id = self.repo.create(data.model_dump())
        return {"status": "success", "id": zone_id}

    def update(self, zona_id, data):
        updates = {k: v for k, v in data.model_dump().items() if v is not None}
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        self.repo.update(zona_id, updates)
        return {"status": "success", "updated": list(updates.keys())}

    def soft_delete(self, zona_id):
        self.repo.soft_delete(zona_id)
        return {"status": "success", "message": "Zona desactivada"}
