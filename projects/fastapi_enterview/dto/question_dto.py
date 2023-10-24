from pydantic import BaseModel


class QuestionDto(BaseModel):
    interview_id: int
    question: str
    type: str