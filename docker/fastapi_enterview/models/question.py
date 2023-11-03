from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from configurations.config import engine, Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    
    interview = relationship("Interview", back_populates="questions")
    
    def __repr__(self):
        return f"<Question(interview_id='{self.interview_id}',question='{self.question}')>"
    
Base.metadata.create_all(bind=engine)