from sqlalchemy.ext.asyncio import AsyncSession
from configurations.config import get_db
from models.question import Question


class QuestionRepository:
    def __init__(self, db: AsyncSession = get_db()):
        self.db = db

    def get_question_by_id(self, question_id: int) -> Question:
        return self.db.query(Question).filter(Question.id == question_id).first()

    def get_all_questions(self) -> list[Question]:
        return self.db.query(Question).all()

    def create_question(self, question: Question) -> Question:
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def update_question(self, question_id: int, question: Question) -> Question:
        question_to_update = self.get_question_by_id(question_id)
        question_to_update.question = question.question
        question_to_update.type = question.type
        self.db.commit()
        self.db.refresh(question_to_update)
        return question_to_update

    def delete_question(self, question_id: int) -> None:
        question_to_delete = self.get_question_by_id(question_id)
        self.db.delete(question_to_delete)
        self.db.commit()