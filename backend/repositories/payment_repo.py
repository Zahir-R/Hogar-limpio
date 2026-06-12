from shared.firebase import db


class PaymentRepository:
    def __init__(self):
        self.collection = db.collection("payments")

    def get(self, reserva_id):
        doc = self.collection.document(reserva_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        data["id"] = doc.id
        return data

    def create(self, reserva_id, data):
        self.collection.document(reserva_id).set(data)

    def update(self, reserva_id, data):
        self.collection.document(reserva_id).update(data)

    def list_all(self):
        return [self._format(d) for d in self.collection.stream()]

    def _format(self, doc):
        data = doc.to_dict()
        data["id"] = doc.id
        return data
