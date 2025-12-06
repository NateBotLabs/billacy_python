# app/services/user_service.py
from app.repositories.repos.user_repository import UserRepository
from app.models.user import User


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def get_all_users(self):
        return self.user_repo.get_all()

    def create_user(self, first_name, last_name, email):
        user = User(first_name=first_name, last_name=last_name, email=email)
        return self.user_repo.insert(user)
