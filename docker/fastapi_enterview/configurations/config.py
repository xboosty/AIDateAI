from sqlalchemy import create_engine
from pydantic_settings import BaseSettings
from typing import List, Any
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
import os

class Settings(BaseSettings):
    DB_USER: str = os.environ['MYSQL_USER']
    DB_PASSWORD: str = os.environ['MYSQL_PASSWORD']
    DB_HOST: str = os.environ['DB_HOST']
    DB_NAME: str = os.environ['MYSQL_DATABASE']
    ALLOWED_HOSTS: Any = os.environ['ALLOWED_HOSTS']

settings = Settings()

# Now, when you need ALLOWED_HOSTS as a list, you can split it:
allowed_hosts_list = settings.ALLOWED_HOSTS.split(',') if ',' in settings.ALLOWED_HOSTS else [settings.ALLOWED_HOSTS]

# Cambia la URL de conexión a MySQL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db  # Proporciona la sesión a la ruta
    finally:
        db.close()
