from sqlalchemy import create_engine
from pydantic_settings import BaseSettings
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker

class Settings(BaseSettings):
    DB_USER: str = "aidate"
    DB_PASSWORD: str = "aidate"
    DB_HOST: str = "localhost"
    DB_NAME: str = "assitantdb"
    ALLOWED_HOSTS: List[str] = ["*"]


settings = Settings()

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db  # Proporciona la sesión a la ruta
    finally:
        db.close()