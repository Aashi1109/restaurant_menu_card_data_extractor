from contextlib import contextmanager

from server.src.database import SessionLocal
from server.src.logger import logger


@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f'Error getting database {str(e)}', exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


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
