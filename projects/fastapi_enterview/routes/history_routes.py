from fastapi import APIRouter, HTTPException
from typing import List
from dto.history_dto import HistoryDto
from configurations.config import get_db

from fastapi import Depends
from sqlalchemy.orm import Session
from models.history import History
from fastapi.responses import JSONResponse

router_history = APIRouter()

@router_history.get(
    "/histories",
    tags=["histories"],
    response_model=List[HistoryDto],
    description="Get a list of all histories",
)
def get_histories(db: Session = Depends(get_db)):
    histories = db.query(History).all()
    return histories


@router_history.get(
    "/histories/{history_id}",
    tags=["histories"],
    response_model=HistoryDto,
    description="Get a history by ID",
)
def get_history(history_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.id == history_id).first()
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return history

@router_history.post(
    "/histories",
    tags=["histories"],
    response_model=HistoryDto,
    description="Create a new history",
)
def create_history(history_create: HistoryDto, db: Session = Depends(get_db)):
    history = History(**history_create.dict())  # Crear una instancia de History a partir de los datos del DTO
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

@router_history.put(
    "/histories/{history_id}",
    tags=["histories"],
    response_model=HistoryDto,
    description="Update a history by ID",
)
def update_history(history_id: int, history_update: HistoryDto, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.id == history_id).first()
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    
    for key, value in history_update.dict().items():
        setattr(history, key, value)

    db.commit()
    db.refresh(history)
    return history

# Eliminar un usuario por ID
@router_history.delete(
    "/histories/{history_id}",
    tags=["histories"],
    response_model=None,
    description="Delete a history by ID",
)
def delete_history(history_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.id == history_id).first()
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")

    db.delete(history)
    db.commit()
    return JSONResponse(content={"message": "History deleted successfully"}, status_code=204)