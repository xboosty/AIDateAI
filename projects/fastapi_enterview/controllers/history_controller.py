from fastapi import APIRouter, HTTPException
from typing import List
from dto.history_dto import HistoryDto
from persistence.history_repository import HistoryRepository
from configurations.config import get_db as async_session
from services.history_service import HistoryService

router = APIRouter()
history_repository = HistoryRepository(async_session())
history_service = HistoryService(history_repository)

@router.post("/historys")
async def create_history(history_dto: HistoryDto):
    try:
        history = history_service.create_history(history_dto)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historys/{history_id}")
async def get_history(history_id: int):
    try:
        history = history_service.get_history(history_id)
        if history is None:
            raise HTTPException(status_code=404, detail="History not found")
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historys")
async def get_all_historys():
    try:
        historys = history_service.get_all_historys()
        return historys
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/historys/{history_id}")
async def update_history(history_id: int, history_dto: HistoryDto):
    try:
        history = history_service.update_history(history_id, history_dto)
        if history is None:
            raise HTTPException(status_code=404, detail="History not found")
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/historys/{history_id}")
async def delete_history(history_id: int):
    try:
        history = history_service.delete_history(history_id)
        if history is None:
            raise HTTPException(status_code=404, detail="History not found")
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))