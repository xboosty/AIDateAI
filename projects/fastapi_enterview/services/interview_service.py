from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.interview import Interview
from dto.interview_dto import InterviewDto
from persistence.interview_repository import InterviewRepository


class InterviewService:
    def __init__(self, db: Session):
        self.db = db
        self.interview_repository = InterviewRepository(db)

    def get_all_interviews(self) -> List[Interview]:
        return self.interview_repository.get_all()

    def get_interview_by_id(self, interview_id: int) -> Interview:
        interview = self.interview_repository.get_by_id(interview_id)
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        return interview

    def create_interview(self, interview_dto: InterviewDto) -> Interview:
        interview = Interview(title=interview_dto.title, 
                              initial_text=interview_dto.initial_text,
                              closure_text=interview_dto.closure_text)
        self.interview_repository.create(interview)
        return interview

    def update_interview(self, interview_id: int, interview_dto: InterviewDto) -> Interview:
        interview = self.get_interview_by_id(interview_id)
        interview.title = interview_dto.title
        interview.initial_text = interview_dto.initial_text
        interview.closure_text = interview_dto.closure_text
        self.interview_repository.update(interview)
        return interview

    def delete_interview(self, interview_id: int) -> None:
        interview = self.get_interview_by_id(interview_id)
        self.interview_repository.delete(interview)