from sqlalchemy.orm import Session
from models.interview import Interview
from dto.interview_dto import InterviewDto


class InterviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_interview(self, interview_dto: InterviewDto):
        interview = Interview(**interview_dto.dict())
        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)
        return interview

    def get_interview_by_id(self, interview_id: int):
        return self.db.query(Interview).filter(Interview.id == interview_id).first()

    def get_all_interviews(self):
        return self.db.query(Interview).all()

    def update_interview(self, interview_id: int, interview_dto: InterviewDto):
        interview = self.get_interview_by_id(interview_id)
        for key, value in interview_dto.dict(exclude_unset=True).items():
            setattr(interview, key, value)
        self.db.commit()
        self.db.refresh(interview)
        return interview

    def delete_interview(self, interview_id: int):
        interview = self.get_interview_by_id(interview_id)
        self.db.delete(interview)
        self.db.commit()
        return interview