from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from server.src.logger import logger
from server.src.scrap.enums import TaskStatus
from server.src.scrap.models import Task


def create_task(db: Session, scrap_query, scrap_data=None, status=TaskStatus.InProgress):
    """
    Creates a new task in the  database with provided params
    :param db: Database connection
    :param scrap_query: Query of the task
    :param scrap_data: Scrap data if available
    :param status: Task status
    :return: Newly created task
    """
    try:
        new_task = Task(
            scrap_query=scrap_query,
            scrap_data=scrap_data,
            status=status
        )

        db.add(new_task)
        db.commit()
        return new_task
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating task: {e}", exc_info=True)
        return None


def get_task_by_id(db: Session, task_id):
    """
    Fetches a task by its ID from the database.
    :param db: Database connection
    :param task_id: ID of the task to fetch
    :return: Task object if found, else None
    """
    try:
        return db.query(Task).filter(Task.id == task_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching task by id: {e}", exc_info=True)
        return None


def get_all_tasks(db: Session):
    """
    Fetches all tasks from the database.
    :param db: Database connection
    :return: List of all tasks if available, else an empty list
    """
    try:
        return db.query(Task).all()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all tasks: {e}", exc_info=True)
        return []


def update_task(db: Session, task_id, scrap_query=None, scrap_data=None, status=None):
    """
    Updates a task in the database with the provided parameters.
    :param db: Database connection
    :param task_id: ID of the task to update
    :param scrap_query: New query for the task
    :param scrap_data: New scrap data for the task
    :param status: New status for the task
    :return: Updated task object if successful, else None
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        if scrap_query:
            task.scrap_query = scrap_query
        if scrap_data:
            task.scrap_data = scrap_data
        if status:
            task.status = status
        db.commit()
        return task
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating task: {e}", exc_info=True)
        return None


def delete_task(db: Session, task_id):
    """
    Deletes a task from the database.
    :param db: Database connection
    :param task_id: ID of the task to delete
    :return: Deleted task object if successful, else None
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        db.delete(task)
        db.commit()
        return task
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting task: {e}", exc_info=True)
        return None
