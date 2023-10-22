from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.question import Question
from dto.question_dto import QuestionDto
from persistence.question_repository import QuestionRepository


class QuestionService:
    def __init__(self, db: Session):
        self.db = db
        self.question_repository = QuestionRepository(db)

    def get_all_questions(self) -> List[Question]:
        return self.question_repository.get_all()

    def get_question_by_id(self, question_id: int) -> Question:
        question = self.question_repository.get_by_id(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question

    def create_question(self, question_dto: QuestionDto) -> Question:
        question = Question(interview_id=question_dto.interview_id, 
                              question=question_dto.question,
                              type=question_dto.type)
        self.question_repository.create(question)
        return question

    def update_question(self, question_id: int, question_dto: QuestionDto) -> Question:
        question = self.get_question_by_id(question_id)
        question.interview_id = question_dto.interview_id
        question.question = question_dto.question
        question.type = question_dto.type
        self.question_repository.update(question)
        return question

    def delete_question(self, question_id: int) -> None:
        question = self.get_question_by_id(question_id)
        self.question_repository.delete(question)