from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from configurations.config import engine, Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True)
    initial_text = Column(String)
    closure_text = Column(String)
    
    users = relationship("User", secondary="histories", back_populates="interviews")
    questions = relationship("Question", back_populates="interview")
    histories = relationship("History", back_populates="interview")
    
    def __repr__(self):
        return f"<Interview(title='{self.title}', initial_text='{self.initial_text}', closure_text='{self.closure_text}')>"
    
Base.metadata.create_all(bind=engine)