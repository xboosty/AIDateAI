from fastapi import APIRouter, HTTPException
from typing import List
from dto.user_dto import UserDto
from configurations.config import get_db
from fastapi.responses import JSONResponse

from fastapi import Depends
from sqlalchemy.orm import Session
from models.user import User

router_user = APIRouter()

@router_user.get(
    "/users",
    tags=["users"],
    response_model=List[UserDto],
    description="Get a list of all users",
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router_user.get(
    "/users/{user_id}",
    tags=["users"],
    response_model=UserDto,
    description="Get a user by ID",
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router_user.post(
    "/users",
    tags=["users"],
    response_model=UserDto,
    description="Create a new user",
)
def create_user(user_create: UserDto, db: Session = Depends(get_db)):
    user = User(**user_create.dict())  # Crear una instancia de User a partir de los datos del DTO
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router_user.put(
    "/users/{user_id}",
    tags=["users"],
    response_model=UserDto,
    description="Update a user by ID",
)
def update_user(user_id: int, user_update: UserDto, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.dict().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

# Eliminar un usuario por ID
@router_user.delete(
    "/users/{user_id}",
    tags=["users"],
    response_model=None,
    description="Delete a user by ID",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return JSONResponse(content={"message": "User deleted successfully"}, status_code=204)
    