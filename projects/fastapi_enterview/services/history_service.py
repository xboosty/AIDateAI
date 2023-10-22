from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.history import History
from dto.history_dto import HistoryDto
from persistence.history_repository import HistoryRepository


class HistoryService:
    def __init__(self, db: Session):
        self.repository = HistoryRepository(db)

    def get_histories(self, user_id: int) -> List[HistoryDto]:
        histories = self.repository.get_histories(user_id)
        return [HistoryDto.from_orm(history) for history in histories]

    def create_history(self, history_dto: HistoryDto) -> HistoryDto:
        created_history = self.repository.create(History(**history_dto.dict()))
        return HistoryDto.from_orm(created_history)

    def delete_history(self, history_id: int):
        deleted_history = self.repository.delete(history_id)
        if not deleted_history:
            raise HTTPException(status_code=404, detail="History item not found")