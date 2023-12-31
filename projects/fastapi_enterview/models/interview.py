from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from configurations.config import engine, Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), unique=True)
    initial_text = Column(String(255))
    closure_text = Column(String(255))
    
    users = relationship("User", secondary="histories", back_populates="interviews")
    questions = relationship("Question", back_populates="interview", cascade="all, delete-orphan")
    histories = relationship("History", back_populates="interview", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Interview(title='{self.title}', initial_text='{self.initial_text}', closure_text='{self.closure_text}')>"
    
Base.metadata.create_all(bind=engine)