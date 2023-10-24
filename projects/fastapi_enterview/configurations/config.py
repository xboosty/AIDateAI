from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DB_USER: str = "aidate"
    DB_PASSWORD: str = "aidate"
    DB_HOST: str = "localhost"
    DB_NAME: str = "assitantdb"
    ALLOWED_HOSTS: List[str] = ["*"]


settings = Settings()

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

def get_db():
    with SessionLocal() as session:
        yield session