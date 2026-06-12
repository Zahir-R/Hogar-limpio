from fastapi import HTTPException, status
from firebase_admin import firestore
from repositories.service_repo import ServiceRepository


class ServiceService:
    def __init__(self):
        self.repo = ServiceRepository()

    def create(self, ofertante_id, data):
        try:
            servicio_data = data.model_dump()
            servicio_data["estado"] = "Pendiente"
            servicio_data["ofertante_id"] = ofertante_id
            servicio_data["created_at"] = firestore.SERVER_TIMESTAMP
            ref = self.repo.create(servicio_data)
            return {"status": "success", "id": ref.id, "message": "Servicio registrado en estado Pendiente"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def list_mine(self, ofertante_id):
        return self.repo.list_by_ofertante(ofertante_id)

    def update(self, servicio_id, ofertante_id, data):
        ref, servicio = self.repo.get(servicio_id)

        if servicio.get("ofertante_id") != ofertante_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para editar este servicio")

        if not any([data.titulo, data.descripcion, data.precio, data.categoria]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Al menos un campo debe ser actualizado")

        actualizacion = {}
        if data.titulo is not None and data.titulo != servicio.get("titulo"):
            actualizacion["titulo"] = data.titulo
            actualizacion["estado"] = "Pendiente"
        if data.precio is not None and data.precio != servicio.get("precio"):
            actualizacion["precio"] = data.precio
            actualizacion["estado"] = "Pendiente"
        if data.descripcion is not None:
            actualizacion["descripcion"] = data.descripcion
        if data.categoria is not None:
            actualizacion["categoria"] = data.categoria

        self.repo.update(servicio_id, actualizacion)
        return {"status": "success", "message": "Servicio actualizado", "updated_fields": actualizacion}

    def delete(self, servicio_id, ofertante_id):
        ref, servicio = self.repo.get(servicio_id)

        if servicio.get("ofertante_id") != ofertante_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para eliminar este servicio")

        if servicio.get("titulo") == "Limpieza básica":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes eliminar el servicio básico")

        self.repo.delete(servicio_id)
        return {"status": "success", "message": "Servicio eliminado"}

    def list_pending(self):
        return self.repo.list_by_estado("Pendiente")

    def validate(self, servicio_id, estado):
        estado = estado.strip().title()
        if estado not in ["Aprobado", "Rechazado"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estado de validación inválido")

        ref, servicio = self.repo.get(servicio_id)
        self.repo.update(servicio_id, {"estado": estado})
        return {"status": "success", "id": servicio_id, "estado": estado}
