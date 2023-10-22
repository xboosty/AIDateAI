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
        users = self.user_repository.get_all()
        return [UserDto.from_orm(user) for user in users]

    def get_user_by_id(self, user_id: int) -> UserDto:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserDto.from_orm(user)

    def create_user(self, user_dto: UserDto) -> UserDto:
        user = User(**user_dto.dict())
        self.user_repository.create(user)
        return UserDto.from_orm(user)

    def update_user(self, user_id: int, user_dto: UserDto) -> UserDto:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user_data = user_dto.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        self.user_repository.save_changes()
        return UserDto.from_orm(user)

    def delete_user(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.user_repository.delete(user)