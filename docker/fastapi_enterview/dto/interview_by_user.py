from pydantic import BaseModel
from typing import List
from .chat_day_by_user import ChatDayByUserDto


class InterviewByUserDto(BaseModel):
    type_question: str
    title: str
    is_complete: bool
    percent_interview: str
    initial_text: str
    closure_text: str
    historial_chat: List[ChatDayByUserDto]
    
