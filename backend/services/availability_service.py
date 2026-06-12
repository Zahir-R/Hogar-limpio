from datetime import date, timedelta
from fastapi import HTTPException, status
from repositories.availability_repo import AvailabilityRepository


class AvailabilityService:
    def __init__(self):
        self.repo = AvailabilityRepository()

    def get(self, worker_uid):
        template = self.repo.get_template(worker_uid)

        today = date.today()
        dates = [(today + timedelta(days=i)).isoformat() for i in range(14)]
        overrides = self.repo.get_overrides_for_range(worker_uid, dates)

        return {"template": template, "overrides": overrides}

    def save_template(self, worker_uid, data):
        self.repo.set_template(worker_uid, data.model_dump())
        return {"status": "success"}

    def toggle_override(self, worker_uid, data):
        if data.worker_uid != worker_uid:
            raise HTTPException(status_code=403, detail="Can only toggle own availability")

        if data.active:
            self.repo.set_override(worker_uid, data.date, {"active": True, "date": data.date})
        else:
            override = self.repo.get_override(worker_uid, data.date)
            if override:
                self.repo.delete_override(worker_uid, data.date)

        return {"status": "success"}
