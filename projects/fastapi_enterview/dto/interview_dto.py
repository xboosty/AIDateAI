from pydantic import BaseModel


class InterviewDto(BaseModel):
    id: int
    title: str
    initial_text: str
    closure_text: str