from repositories.user_repo import UserRepository
from firebase_admin import auth, firestore

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register_new_user(self, firebase_user: dict, request_body: dict = None) -> dict:
        uid = firebase_user["uid"]
        email = firebase_user.get("email")
        role = "cliente"
        display_name = firebase_user.get("name")
        
        if request_body:
            role = request_body.get("role", "cliente")
            display_name = request_body.get("display_name", display_name)

        user_data = {
            "uid": uid,
            "email": email,
            "display_name": display_name,
            "role": role,
            "created_at": firestore.SERVER_TIMESTAMP
        }

        self.repo.save_user(user_data)
        auth.set_custom_user_claims(uid, {"role": role})
        user_data.pop("created_at", None)
        return user_data
    
    def update_user_role(self, uid: str, new_role: str) -> None:
        self.repo.collection.document(uid).update({"role": new_role})
        auth.set_custom_user_claims(uid, {"role": new_role})
