from fastapi import APIRouter, HTTPException
from typing import List
from dto.question_dto import QuestionDto
from configurations.config import get_db

from fastapi import Depends
from sqlalchemy.orm import Session
from models.question import Question
from fastapi.responses import JSONResponse

router_question = APIRouter()

@router_question.get(
    "/questions",
    tags=["questions"],
    response_model=List[QuestionDto],
    description="Get a list of all questions",
)
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions


@router_question.get(
    "/questions/{question_id}",
    tags=["questions"],
    response_model=QuestionDto,
    description="Get a question by ID",
)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router_question.post(
    "/questions",
    tags=["questions"],
    response_model=QuestionDto,
    description="Create a new question",
)
def create_question(question_create: QuestionDto, db: Session = Depends(get_db)):
    question = Question(**question_create.dict())  # Crear una instancia de Question a partir de los datos del DTO
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

@router_question.put(
    "/questions/{question_id}",
    tags=["questions"],
    response_model=QuestionDto,
    description="Update a question by ID",
)
def update_question(question_id: int, question_update: QuestionDto, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    
    for key, value in question_update.dict().items():
        setattr(question, key, value)

    db.commit()
    db.refresh(question)
    return question

# Eliminar un usuario por ID
@router_question.delete(
    "/questions/{question_id}",
    tags=["questions"],
    response_model=None,
    description="Delete a question by ID",
)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()
    return JSONResponse(content={"message": "Question deleted successfully"}, status_code=204)