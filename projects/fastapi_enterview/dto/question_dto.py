from pydantic import BaseModel


class QuestionDtoIn(BaseModel):
    interview_id: int
    question: str
    type: str
    
class QuestionDtoOut(BaseModel):
    id: int
    interview_id: int
    question: str
    type: str