from pydantic import BaseModel

class UserDtoIn(BaseModel):
    email: str
    avatar: str
    
class UserDtoOut(BaseModel):
    id: int
    email: str
    avatar: str