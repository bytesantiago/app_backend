from domain.ports.user_repository import UserRepository
from sqlalchemy.orm import Session
from infrastructure.orm.user_model import UserModel

class UserRepositorySQLAlchemy(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data):
        new_user = UserModel(**user_data)
        self.session.add(new_user)
        self.session.commit()
        return new_user
