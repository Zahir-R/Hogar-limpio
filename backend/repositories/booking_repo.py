from fastapi import HTTPException, status
from shared.firebase import db


class BookingRepository:
    def __init__(self):
        self.collection = db.collection("reservas")

    def get(self, reserva_id):
        ref = self.collection.document(reserva_id)
        doc = ref.get()
        if not doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        data = doc.to_dict()
        data["id"] = doc.id
        return ref, data

    def create(self, data):
        ref = self.collection.add(data)
        return ref[1]

    def list_by_client(self, uid):
        return [self._format(d) for d in self.collection.where("cliente_uid", "==", uid).stream()]

    def list_by_worker(self, uid):
        return [self._format(d) for d in self.collection.where("worker_uid", "==", uid).stream()]

    def list_all(self):
        return [self._format(d) for d in self.collection.stream()]

    def update(self, reserva_id, data):
        self.collection.document(reserva_id).update(data)

    def find_completed(self, cliente_uid, worker_uid):
        docs = (
            self.collection
            .where("cliente_uid", "==", cliente_uid)
            .where("worker_uid", "==", worker_uid)
            .where("estado", "==", "Completado")
            .stream()
        )
        return docs

    def _format(self, doc):
        data = doc.to_dict()
        data["id"] = doc.id
        return data
