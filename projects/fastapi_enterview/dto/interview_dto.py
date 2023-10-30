from pydantic import BaseModel


class InterviewDtoIn(BaseModel):
    title: str
    initial_text: str
    closure_text: str
    
class InterviewDtoOut(BaseModel):
    id: int
    title: str
    initial_text: str
    closure_text: str