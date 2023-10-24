from fastapi import APIRouter, HTTPException
from typing import List
from dto.user_dto import UserDto
from persistence.user_repository import UserRepository
from configurations.config import get_db as async_session
from services.user_service import UserService

router = APIRouter()

user_repository = UserRepository(async_session())
service = UserService(user_repository)

@router.post("/users")
async def create_user(user: UserDto):
    try:
        created_user = service.create_user(user)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users")
async def read_users():
    try:
        users = service.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    try:
        user = service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/users/{user_id}")
async def update_user(user_id: int, user: UserDto):
    try:
        updated_user = service.update_user(user_id, user)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    try:
        deleted_user = service.delete_user(user_id)
        if deleted_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return deleted_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))