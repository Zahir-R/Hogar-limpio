from fastapi import HTTPException, status
from firebase_admin import firestore
from repositories.booking_repo import BookingRepository
from repositories.payment_repo import PaymentRepository
from services.pricing_service import PricingService


VALID_TRANSITIONS = {
    "Pendiente": ["Confirmado", "Cancelado"],
    "Confirmado": ["En_curso", "Completado", "Cancelado"],
    "En_curso": ["Completado"],
    "Completado": [],
    "Cancelado": []
}


class BookingService:
    def __init__(self):
        self.repo = BookingRepository()
        self.payment_repo = PaymentRepository()
        self.pricing_service = PricingService()

    def create(self, cliente_uid, data):
        total = self.pricing_service.calculate(data.rooms, data.sqm, data.zona)
        reserva_data = {
            "cliente_uid": cliente_uid,
            "worker_uid": data.worker_uid,
            "servicio_ids": data.servicio_ids,
            "servicio_id": data.servicio_ids[0] if data.servicio_ids else "",
            "fecha": data.fecha,
            "hora_inicio": data.hora_inicio,
            "duracion_horas": data.duracion_horas,
            "direccion": data.direccion,
            "zona": data.zona,
            "precio_total": total,
            "estado": "Pendiente",
            "recurrencia": "none",
            "rooms": data.rooms,
            "sqm": data.sqm,
            "created_at": firestore.SERVER_TIMESTAMP,
            "completed_at": None
        }
        ref = self.repo.create(reserva_data)
        return {"status": "success", "id": ref.id, "precio_total": total}

    def list(self, uid, role):
        if role == "cliente":
            return self.repo.list_by_client(uid)
        elif role == "personal_limpieza":
            return self.repo.list_by_worker(uid)
        elif role == "admin":
            return self.repo.list_all()
        raise HTTPException(status_code=403, detail="Unknown role")

    def confirm(self, reserva_id, worker_uid):
        ref, reserva = self.repo.get(reserva_id)
        if reserva["worker_uid"] != worker_uid:
            raise HTTPException(status_code=403, detail="Not your reservation")
        return self._transition(reserva_id, "Confirmado")

    def complete(self, reserva_id, cliente_uid):
        ref, reserva = self.repo.get(reserva_id)
        if reserva["cliente_uid"] != cliente_uid:
            raise HTTPException(status_code=403, detail="Not your reservation")
        return self._transition(reserva_id, "Completado")

    def cancel(self, reserva_id, user):
        uid = user["uid"]
        role = user.get("role")
        ref, reserva = self.repo.get(reserva_id)
        if role != "admin" and reserva["cliente_uid"] != uid and reserva["worker_uid"] != uid:
            raise HTTPException(status_code=403, detail="Not authorized to cancel")
        return self._transition(reserva_id, "Cancelado")

    def _transition(self, reserva_id, new_state):
        ref, reserva = self.repo.get(reserva_id)
        current = reserva["estado"]

        if new_state not in VALID_TRANSITIONS.get(current, []):
            raise HTTPException(
                status_code=400,
                detail=f"Cannot transition from {current} to {new_state}"
            )

        updates = {"estado": new_state}
        if new_state == "Completado":
            updates["completed_at"] = firestore.SERVER_TIMESTAMP
        self.repo.update(reserva_id, updates)

        if new_state == "Confirmado":
            self.payment_repo.create(reserva_id, {
                "reserva_id": reserva_id,
                "cliente_uid": reserva["cliente_uid"],
                "worker_uid": reserva["worker_uid"],
                "monto": reserva.get("precio_total", 0),
                "comision": round(reserva.get("precio_total", 0) * 0.10, 2),
                "metodo": "qr",
                "estado": "Retenido",
                "created_at": firestore.SERVER_TIMESTAMP,
                "released_at": None
            })
        elif new_state == "Completado":
            pay = self.payment_repo.get(reserva_id)
            if pay:
                self.payment_repo.update(reserva_id, {
                    "estado": "Liberado",
                    "released_at": firestore.SERVER_TIMESTAMP
                })
        elif new_state == "Cancelado":
            pay = self.payment_repo.get(reserva_id)
            if pay:
                self.payment_repo.update(reserva_id, {"estado": "Reembolsado"})

        return {"status": "success", "id": reserva_id, "estado": new_state}

    def get_payment(self, reserva_id, user):
        ref, reserva = self.repo.get(reserva_id)
        uid = user["uid"]
        role = user.get("role")
        if role != "admin" and reserva["cliente_uid"] != uid and reserva["worker_uid"] != uid:
            raise HTTPException(status_code=403, detail="Not authorized")
        pay = self.payment_repo.get(reserva_id)
        return pay
