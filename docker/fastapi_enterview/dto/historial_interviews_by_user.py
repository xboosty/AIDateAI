from pydantic import BaseModel
from typing import List
from .interview_by_user import InterviewByUserDto


class HistorialInterviewsByUserDto(BaseModel):
    user_id: int
    result: List[InterviewByUserDto]