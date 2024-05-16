from sqlalchemy.orm import Session

from domain.models.user import User
from domain.ports.user_repository import UserRepository


class UserRepositorySQLAlchemy(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data):
        new_user = User(**user_data)
        self.session.add(new_user)
        self.session.commit()
        return new_user
