from pydantic import BaseModel
from models.history import PyEnum


class HistoryDto(BaseModel):
    id: int
    user_id: int
    interview_id: int
    message: str
    status_message: PyEnum
    hour: str
    is_response: bool
    audio: bytes