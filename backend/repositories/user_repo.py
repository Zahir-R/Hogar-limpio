class UserRepository:
    def save_user(self, user_data: dict):
        print(f"Saving user {user_data['email']} tot the local database...")
        return user_data