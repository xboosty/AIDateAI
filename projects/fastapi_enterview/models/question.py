from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question = Column(String, nullable=False)
    type = Column(String, nullable=False)
    
    interview = relationship("Interview", back_populates="questions")
    
    def __repr__(self):
        return f"<Question(interview_id='{self.interview_id}',question='{self.question}')>"