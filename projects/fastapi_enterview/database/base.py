from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from configurations.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base = declarative_base()