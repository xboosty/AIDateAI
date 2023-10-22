from sqlalchemy.orm import Session
from database.session import get_db
from models.history import History


class historyRepository:
    def __init__(self, db: Session = get_db()):
        self.db = db

    def get_all_histories(self):
        return self.db.query(History).all()

    def get_history_by_id(self, history_id: int):
        return self.db.query(History).filter(History.id == history_id).first()

    def create_history(self, history):
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def update_history(self, history_id: int, history):
        history_to_update = self.get_history_by_id(history_id)
        history_to_update.name = history.name
        history_to_update.description = history.description
        history_to_update.price = history.price
        self.db.commit()
        self.db.refresh(history_to_update)
        return history_to_update

    def delete_history(self, history_id: int):
        history_to_delete = self.get_history_by_id(history_id)
        self.db.delete(history_to_delete)
        self.db.commit()
        return history_to_delete