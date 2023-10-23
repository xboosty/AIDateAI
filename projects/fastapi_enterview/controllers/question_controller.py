from fastapi import APIRouter, HTTPException
from typing import List
from dto.question_dto import QuestionDto
from persistence.question_repository import QuestionRepository
from configurations.config import get_db as async_session
from services.question_service import QuestionService

router = APIRouter()
question_repository = QuestionRepository(async_session())
question_service = QuestionService(question_repository)

@router.post("/questions")
async def create_question(question_dto: QuestionDto):
    try:
        question = question_service.create_question(question_dto)
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/questions/{question_id}")
async def get_question(question_id: int):
    try:
        question = question_service.get_question(question_id)
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/questions")
async def get_all_questions():
    try:
        questions = question_service.get_all_questions()
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/questions/{question_id}")
async def update_question(question_id: int, question_dto: QuestionDto):
    try:
        question = question_service.update_question(question_id, question_dto)
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/questions/{question_id}")
async def delete_question(question_id: int):
    try:
        question = question_service.delete_question(question_id)
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))