from shared.firebase import db


class PricingRepository:
    def __init__(self):
        self.doc_ref = db.collection("config").document("pricing")

    def get(self):
        doc = self.doc_ref.get()
        return doc.to_dict() if doc.exists else None

    def set(self, data):
        self.doc_ref.set(data, merge=True)
