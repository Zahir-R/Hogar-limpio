from fastapi import HTTPException
from firebase_admin import firestore
from repositories.pricing_repo import PricingRepository
from repositories.zone_repo import ZoneRepository


class PricingService:
    def __init__(self):
        self.repo = PricingRepository()
        self.zone_repo = ZoneRepository()

    def calculate(self, rooms: int, sqm: float, zona: str = None) -> float:
        config = self.repo.get()
        if config:
            base_rate = config.get("base_rate", 30)
            room_rate = config.get("room_rate", 15)
            sqm_rate = config.get("sqm_rate", 0.5)
        else:
            base_rate, room_rate, sqm_rate = 30, 15, 0.5

        total = base_rate + (rooms * room_rate) + (sqm * sqm_rate)

        if zona:
            surcharge = self.zone_repo.find_by_nombre(zona)
            total += total * surcharge

        return round(total, 2)

    def get_config(self):
        config = self.repo.get()
        if not config:
            return {
                "base_rate": 30, "room_rate": 15, "sqm_rate": 0.5,
                "zone_surcharge_enabled": True, "currency": "BOB"
            }
        config.pop("updated_at", None)
        return config

    def update_config(self, admin_uid, data):
        payload = data.model_dump()
        payload["updated_at"] = firestore.SERVER_TIMESTAMP
        payload["updated_by"] = admin_uid
        self.repo.set(payload)
        return {"status": "success"}
