from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from configurations.config import engine, Base
from datetime import datetime
from .question import Question

class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    message = Column(String(255), nullable=False)
    status_message = Column(String(8), nullable=False)
    date = Column(DateTime, default=datetime.now())
    hour = Column(String(10), nullable=False)
    is_response = Column(Boolean, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    audio = Column(String(255), nullable=True) #mejor guardar el audio en un bucket de S3,se llena si is_response es True
    
    __table_args__ = (
        CheckConstraint(status_message.in_(["SENT", "RECEIVED", "ERROR"])),
    )
    
    user = relationship("User", back_populates="histories")
    interview = relationship("Interview", back_populates="histories")
    
    def __repr__(self):
        return f"<Interview(user_id='{self.user_id}',interview_id='{self.interview_id}', message='{self.message}')>"
    
    def related_question(self, db):
        if self.question_id is not None:
            return db.query(Question).filter(Question.id == self.question_id).first()
        return None
    
Base.metadata.create_all(bind=engine)