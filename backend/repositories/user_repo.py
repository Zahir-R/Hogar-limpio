from shared.firebase import db


class UserRepository:
    def __init__(self):
        self.collection = db.collection("users")

    def get(self, uid):
        doc = self.collection.document(uid).get()
        if not doc.exists:
            return None
        return self._format(doc)

    def list_by_role(self, role, zona=None):
        query = self.collection.where("role", "==", role)
        if zona:
            query = query.where("zona", "==", zona)
        return [self._format(d) for d in query.stream()]

    def list_all(self):
        return [self._format(d) for d in self.collection.stream()]

    def update(self, uid, data):
        self.collection.document(uid).update(data)

    def set(self, uid, data, merge=True):
        self.collection.document(uid).set(data, merge=merge)

    def delete(self, uid):
        self.collection.document(uid).delete()

    def get_subcollection(self, uid, subcol):
        return self.collection.document(uid).collection(subcol).stream()

    def get_subcollection_doc(self, uid, subcol, doc_id):
        return self.collection.document(uid).collection(subcol).document(doc_id).get()

    def add_to_subcollection(self, uid, subcol, data):
        return self.collection.document(uid).collection(subcol).add(data)

    def stream_all_with_role(self, role):
        return self.collection.where("role", "==", role).stream()

    def _format(self, doc):
        data = doc.to_dict()
        data["uid"] = doc.id
        data.pop("created_at", None)
        return data
