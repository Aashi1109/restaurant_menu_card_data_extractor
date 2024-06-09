from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import declarative_base, sessionmaker

from server.src.config import SQLALCHEMY_DATABASE_URL

# connect_args required only for sqlite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=NullPool)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db():
    Base.metadata.create_all(bind=engine)
