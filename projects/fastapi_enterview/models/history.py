from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from database.base import Base

class StatusEnum(PyEnum):
    SENT = "SENT"
    RECEIVED = "RECEIVED"
    ERROR = "ERROR"


class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), primary_key=True)
    message = Column(String, nullable=False)
    status_message = Column(PyEnum(StatusEnum), nullable=False)
    hour = Column(String, nullable=False)
    is_response = Column(Boolean, nullable=False)
    audio = Column(LargeBinary, nullable=True)
    
    user = relationship("User", back_populates="histories")
    interview = relationship("Interview", back_populates="histories")
    
    def __repr__(self):
        return f"<Interview(user_id='{self.user_id}',interview_id='{self.interview_id}', message='{self.message}')>"