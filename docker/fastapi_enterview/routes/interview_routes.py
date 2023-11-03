from fastapi import APIRouter, HTTPException
from typing import List
from dto.interview_dto import InterviewDtoIn, InterviewDtoOut
from configurations.config import get_db

from fastapi import Depends
from sqlalchemy.orm import Session
from models.interview import Interview
from fastapi.responses import JSONResponse
from .security import oauth2_scheme

router_interview = APIRouter()

@router_interview.get(
    "/interviews",
    tags=["interviews"],
    response_model=List[InterviewDtoOut],
    description="Get a list of all interviews",
)
def get_interviews(db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    interviews = db.query(Interview).all()
    return interviews


@router_interview.get(
    "/interviews/{interview_id}",
    tags=["interviews"],
    response_model=InterviewDtoOut,
    description="Get a interview by ID",
)
def get_interview(interview_id: int, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview

@router_interview.post(
    "/interviews",
    tags=["interviews"],
    response_model=InterviewDtoOut,
    description="Create a new interview",
)
def create_interview(interview_create: InterviewDtoIn, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    interview = Interview(**interview_create.dict())  # Crear una instancia de Interview a partir de los datos del DTO
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview

@router_interview.put(
    "/interviews/{interview_id}",
    tags=["interviews"],
    response_model=InterviewDtoOut,
    description="Update a interview by ID",
)
def update_interview(interview_id: int, interview_update: InterviewDtoIn, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    for key, value in interview_update.dict().items():
        setattr(interview, key, value)

    db.commit()
    db.refresh(interview)
    return interview

# Eliminar un usuario por ID
@router_interview.delete(
    "/interviews/{interview_id}",
    tags=["interviews"],
    response_model=None,
    description="Delete a interview by ID",
)
def delete_interview(interview_id: int, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")

    db.delete(interview)
    db.commit()
    return JSONResponse(content={"message": "Interview deleted successfully"}, status_code=204)