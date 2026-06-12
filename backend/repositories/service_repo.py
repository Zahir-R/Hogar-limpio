from fastapi import HTTPException, status
from shared.firebase import db


class ServiceRepository:
    def __init__(self):
        self.collection = db.collection("servicios")

    def get(self, servicio_id):
        ref = self.collection.document(servicio_id)
        doc = ref.get()
        if not doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado"
            )
        data = doc.to_dict()
        data["id"] = doc.id
        return ref, data

    def list_by_ofertante(self, ofertante_id):
        docs = self.collection.where("ofertante_id", "==", ofertante_id).stream()
        return [self._format(d) for d in docs]

    def list_by_estado(self, estado):
        docs = self.collection.where("estado", "==", estado).stream()
        return [self._format(d) for d in docs]

    def list_approved_by_ofertante(self, ofertante_id):
        docs = (
            self.collection
            .where("ofertante_id", "==", ofertante_id)
            .where("estado", "==", "Aprobado")
            .stream()
        )
        return [self._format(d) for d in docs]

    def create(self, data):
        ref, doc = self.collection.add(data)
        return ref

    def update(self, servicio_id, data):
        self.collection.document(servicio_id).update(data)

    def delete(self, servicio_id):
        self.collection.document(servicio_id).delete()

    def exists(self, field, value, filter_field, filter_value):
        docs = (
            self.collection
            .where(field, "==", value)
            .where(filter_field, "==", filter_value)
            .stream()
        )
        return any(docs)

    def _format(self, doc):
        data = doc.to_dict()
        data["id"] = doc.id
        return data
