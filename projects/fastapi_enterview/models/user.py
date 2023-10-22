from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    avatar = Column(String, nullable=False)
    
    interviews = relationship("Interview", secondary="histories", back_populates="users")
    histories = relationship("History", back_populates="user")
    
    def __repr__(self):
        return f"<User(email='{self.email}', avatar='{self.avatar}')>"