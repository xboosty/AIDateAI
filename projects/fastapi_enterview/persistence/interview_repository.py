from sqlalchemy.ext.asyncio import AsyncSession
from configurations.config import get_db
from models.interview import Interview


class InterviewRepository:
    def __init__(self, db: AsyncSession = get_db()):
        self.db = db

    def get_all_histories(self):
        return self.db.query(Interview).all()

    def get_interview_by_id(self, interview_id: int):
        return self.db.query(Interview).filter(Interview.id == interview_id).first()

    def create_interview(self, interview):
        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)
        return interview

    def update_interview(self, interview_id: int, interview):
        interview_to_update = self.get_interview_by_id(interview_id)
        interview_to_update.title = interview.title
        interview_to_update.initial_text = interview.initial_text
        interview_to_update.closure_text = interview.closure_text
        self.db.commit()
        self.db.refresh(interview_to_update)
        return interview_to_update

    def delete_interview(self, interview_id: int):
        interview_to_delete = self.get_interview_by_id(interview_id)
        self.db.delete(interview_to_delete)
        self.db.commit()
        return interview_to_delete