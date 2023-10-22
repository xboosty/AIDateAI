from pydantic import BaseModel


class QuestionDto(BaseModel):
    id: int
    interview_id: int
    question: str
    type: str