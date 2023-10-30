from pydantic import BaseModel

class MessageByUserDto(BaseModel):
    email: str
    message: str
    status_message: str
    hour: str
    is_bot: bool #contrario a is_response
    audio: bytes
    
