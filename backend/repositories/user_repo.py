from google.cloud.firestore import Client
from firebase_admin import firestore

class UserRepository:
    def __init__(self):
        self.db = firestore.client()
        self.collection = self.db.collection("users")

    def save_user(self, user_data: dict) -> dict:
        doc_ref = self.collection.document(user_data["uid"])
        doc_ref.set(user_data, merge=True)
        return user_data