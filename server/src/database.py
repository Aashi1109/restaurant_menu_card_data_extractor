from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from server.src.logger import logger

engine = create_engine('sqlite:///tasks.db')

Base = declarative_base()

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = Session()
    try:
        yield db
    except Exception as e:
        logger.error(f'Error getting database {str(e)}', exc_info=True)
        db.rollback()
    finally:
        db.close()
