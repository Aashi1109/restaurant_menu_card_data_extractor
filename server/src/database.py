from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from server.src.config import SQLALCHEMY_DATABASE_URL
from server.src.logger import logger

# connect args required only for sqlite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f'Error getting database {str(e)}', exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()
