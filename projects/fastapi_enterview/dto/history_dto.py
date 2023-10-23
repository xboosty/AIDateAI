from pydantic import BaseModel


class HistoryDto(BaseModel):
    id: int
    user_id: int
    interview_id: int
    message: str
    status_message: str
    hour: str
    is_response: bool
    audio: bytes