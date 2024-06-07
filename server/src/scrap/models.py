from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, func

from server.src.database import Base
from server.src.scrap.enums import TaskStatus


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    scrap_query = Column(String, nullable=False)
    scrap_data = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.InProgress, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
