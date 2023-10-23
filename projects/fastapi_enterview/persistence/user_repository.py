from sqlalchemy.ext.asyncio import AsyncSession
from configurations.config import get_db
from models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession = get_db()):
        self.db = db

    def get_all_users(self):
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, user):
        user_to_update = self.get_user_by_id(user_id)
        user_to_update.email = user.email
        user_to_update.avatar = user.avatar
        self.db.commit()
        self.db.refresh(user_to_update)
        return user_to_update

    def delete_user(self, user_id: int):
        user_to_delete = self.get_user_by_id(user_id)
        self.db.delete(user_to_delete)
        self.db.commit()
        return user_to_delete