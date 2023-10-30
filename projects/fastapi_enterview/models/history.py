from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, LargeBinary, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from configurations.config import engine, Base
from datetime import datetime

class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    message = Column(String, nullable=False)
    status_message = Column(String(length=8), nullable=False)
    date = Column(DateTime, default=datetime.now())
    hour = Column(String, nullable=False)
    is_response = Column(Boolean, nullable=False)
    audio = Column(LargeBinary, nullable=True)
    
    __table_args__ = (
        CheckConstraint(status_message.in_(["SENT", "RECEIVED", "ERROR"])),
    )
    
    user = relationship("User", back_populates="histories")
    interview = relationship("Interview", back_populates="histories")
    
    def __repr__(self):
        return f"<Interview(user_id='{self.user_id}',interview_id='{self.interview_id}', message='{self.message}')>"
    
Base.metadata.create_all(bind=engine)