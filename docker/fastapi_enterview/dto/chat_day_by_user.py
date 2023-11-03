from pydantic import BaseModel
from typing import List
from .message_by_user import MessageByUserDto


class ChatDayByUserDto(BaseModel):
    day: str    
    messages: List[MessageByUserDto]