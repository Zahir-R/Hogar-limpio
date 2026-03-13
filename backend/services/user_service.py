from repositories.user_repo import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register_new_user(self, firebase_user: dict):
        user_data = {
            "uid": firebase_user["uid"],
            "email": firebase_user.get("email"),
            "display_name": firebase_user.get("name")
        }
        return self.repo.save_user(user_data)