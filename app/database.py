from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

DATABASE_URL = (
    "postgresql+psycopg2://"
    + settings.DB_USER
    + ":"
    + settings.DB_PASSWORD
    + "@"
    + settings.DB_HOST
    + ":"
    + str(settings.DB_PORT)
    + "/"
    + settings.DB_NAME
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
