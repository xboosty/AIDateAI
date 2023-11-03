from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class HistoryDtoIn(BaseModel):
    user_id: int
    interview_id: int
    message: Optional[str] = None
    is_response: bool
    question_id: int
    
class HistoryDtoOut(BaseModel):
    id: int
    user_id: int
    interview_id: int
    message: str
    status_message: str
    date: datetime
    hour: str
    is_response: bool
    question_id: int
    audio: Optional[str] = None