from shared.firebase import db


class ReviewRepository:
    def __init__(self):
        self.collection = db.collection("reviews")

    def create(self, data):
        return self.collection.add(data)

    def list_by_worker(self, worker_uid):
        docs = self.collection.where("worker_uid", "==", worker_uid).stream()
        result = []
        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            client_doc = db.collection("users").document(item["client_uid"]).get()
            if client_doc.exists:
                item["clientName"] = client_doc.to_dict().get("displayName", "Cliente")
            else:
                item["clientName"] = "Cliente"
            result.append(item)
        return result
