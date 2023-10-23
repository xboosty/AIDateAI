from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from dto.user_dto import UserDto
from persistence.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_all_users(self) -> List[UserDto]:
        users = self.user_repository.get_all_users()
        return [UserDto.from_orm(user) for user in users]

    def get_user_by_id(self, user_id: int) -> UserDto:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserDto.from_orm(user)

    def create_user(self, user_dto: UserDto) -> UserDto:
        user = User(email=user_dto.email, avatar=user_dto.avatar)
        self.user_repository.create_user(user)
        return user

    def update_user(self, user_id: int, user_dto: UserDto) -> UserDto:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        updated_user = self.user_repository.update_user(user_id, user_dto)
        return updated_user

    def delete_user(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.user_repository.delete_user(user)