from pydantic import BaseModel
from datetime import datetime


class HistoryDto(BaseModel):
    user_id: int
    interview_id: int
    message: str
    status_message: str
    date: datetime
    hour: str
    is_response: bool
    audio: bytes