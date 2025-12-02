import os
from sqlalchemy import create_engine
from .models.base import Base
from sqlalchemy.orm import Session, sessionmaker

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST= os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")

DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_DATABASE}'


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit() #commit changes
    except Exception:
        db.rollback() #rollback on errors
        raise
    finally:
        db.close()

