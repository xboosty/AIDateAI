from pydantic import BaseModel

class UserDto(BaseModel):
    id: int
    email: str
    avatar: str