from domain.models.user import User
from domain.ports.user_repository import UserRepository

class CreateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_data):
        new_user = User(**user_data)
        self.repository.create_user(new_user)
        return new_user
