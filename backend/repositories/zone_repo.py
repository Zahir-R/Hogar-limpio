from shared.firebase import db


class ZoneRepository:
    def __init__(self):
        self.collection = db.collection("zonas")

    def list_active(self):
        docs = self.collection.where("active", "==", True).stream()
        return [self._format(d) for d in docs]

    def list_all(self):
        return [self._format(d) for d in self.collection.stream()]

    def create(self, data):
        ref = self.collection.add(data)
        return ref[1].id

    def update(self, zona_id, data):
        self.collection.document(zona_id).update(data)

    def soft_delete(self, zona_id):
        self.collection.document(zona_id).update({"active": False})

    def find_by_nombre(self, nombre):
        docs = (
            self.collection
            .where("nombre", "==", nombre)
            .where("active", "==", True)
            .stream()
        )
        for doc in docs:
            return doc.to_dict().get("surcharge", 0)
        return 0

    def _format(self, doc):
        data = doc.to_dict()
        data["id"] = doc.id
        return data
