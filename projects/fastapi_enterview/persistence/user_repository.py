from sqlalchemy.orm import Session
from database.user import UserModel
from dto.user_dto import UserDto


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_dto: UserDto):
        user = UserModel(**user_dto.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_all_users(self):
        return self.db.query(UserModel).all()

    def update_user(self, user_id: int, user_dto: UserDto):
        user = self.get_user_by_id(user_id)
        for key, value in user_dto.dict(exclude_unset=True).items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        self.db.delete(user)
        self.db.commit()
        return user