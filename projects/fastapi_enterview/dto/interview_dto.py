from pydantic import BaseModel


class InterviewDto(BaseModel):
    title: str
    initial_text: str
    closure_text: str