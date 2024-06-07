from fastapi import APIRouter

from server.src.database import get_db
from server.src.logger import logger
from server.src.scrap.models import Task
from server.src.scrap.schemas import ScrapRequest
from server.src.tasks import scrap_get_search_results_scheduler

router = APIRouter()


@router.post("/submit")
async def create_new_scrap(_data: ScrapRequest):
    try:
        # create new entry in task table and return that entry to user
        new_task = Task(scrap_query=_data.query)
        with get_db() as session:
            session.add(new_task)
            session.commit()
            session.refresh(new_task)

        # call celery background task manager to handle tasks
        scrap_get_search_results_scheduler(_data.query, _data.max_links, _data.use_cse_papi, _data.__repr__())

        return {"success": True, "message": "Scrap task created successfully", "data": {"task_id": new_task.id}}

    except Exception as e:
        logger.error(f"Error submitting data {e}", exc_info=True)


@router.get("/status/{id}")
async def get_scrap_status(id: int):
    try:
        with get_db() as session:
            task = session.query(Task).filter(Task.id == id).first()
            if not task:
                return {"success": False, "message": "Task not found", "data": None}

            return {"success": True, "message": "Task found", "data": {"status": task.status}}

    except Exception as e:
        logger.error(f"Error submitting data {e}", exc_info=True)
