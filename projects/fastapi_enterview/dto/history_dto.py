from pydantic import BaseModel


class HistoryDto(BaseModel):
    user_id: int
    interview_id: int
    message: str
    status_message: str
    hour: str
    is_response: bool
    audio: bytes