from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from server.src.SessionLocal import get_db
from server.src.logger import logger
from server.src.scrap.crud import create_task, get_task_by_id, get_all_tasks, delete_task, update_task
from server.src.scrap.schemas import ScrapSubmitRequest, ScrapResponse, ScrapAllTasksResponse, TaskUpdateRequest
from server.src.worker import scrap_save_search_results_worker

router = APIRouter()


@router.post("/scrap/new", response_model=ScrapResponse, status_code=201)
async def create_new_scrap(req: Request, _data: ScrapSubmitRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Request received url: {str(req.url)}, req body: {str(_data.model_dump())}")

        # create new entry in task table and return that entry to user
        create_task_result = create_task(db, _data.query)

        if not create_task_result:
            raise Exception("Failed to create task entry")

        # call celery background task manager to handle tasks
        scrap_save_search_results_worker.s(
            _data.query, _data.max_links, _data.use_cse_papi,
            {"request": _data.__repr__(), "db": create_task_result.to_dict()}
        ).apply_async()

        return ScrapResponse(
            success=True, message="Scrap task created successfully", data={"task_id": create_task_result.id}
        )

    except Exception as e:
        logger.error(f"Error creating task {e}", exc_info=True)


@router.get("/scrap/tasks", response_model=ScrapAllTasksResponse)
async def get_all_tasks_handler(req: Request, db: Session = Depends(get_db)):
    try:
        logger.info(f"Request received url: {str(req.url)}")

        tasks = get_all_tasks(db)

        if not tasks:
            return ScrapAllTasksResponse(success=False, message="No task found", data=[])
        tasks = [task.to_dict() for task in tasks]

        return ScrapAllTasksResponse(
            success=True, message="Tasks found", data=tasks
        )

    except Exception as e:
        logger.error(f"Error getting tasks data {e}", exc_info=True)


@router.get("/scrap/{task_id}", response_model=ScrapResponse)
async def get_scrap_status(req: Request, task_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Request received url: {str(req.url)}, req body: {str(req.query_params)}")

        existing_task = get_task_by_id(db, task_id)
        if not existing_task:
            return ScrapResponse(success=False, message="Task not found", data=None)

        return ScrapResponse(
            success=True, message="Task found", data={"status": existing_task.status, "task": existing_task.to_dict()}
        )

    except Exception as e:
        logger.error(f"Error getting data for task {e}", exc_info=True)


@router.delete("/scrap/{task_id}", response_model=ScrapResponse)
async def delete_task_handler(req: Request, task_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Request received url: {str(req.url)}, req body: {str(req.query_params)}")

        existing_task = delete_task(db, task_id)
        if not existing_task:
            return ScrapResponse(success=False, message="Task not found with provided id", data=None)

        return ScrapResponse(
            success=True, message="Task delete successfully", data=existing_task.to_dict()
        )

    except Exception as e:
        logger.error(f"Error deleting task data {e}", exc_info=True)


@router.patch("/scrap/{task_id}", response_model=ScrapResponse)
async def update_task_handler(req: Request, task_id: int, _data: TaskUpdateRequest, db: Session = Depends(get_db)):
    try:
        logger.info(
            f"Request received url: {str(req.url)}, req data params: {str(req.query_params)} body: {str(req.body)}")

        updated_task = update_task(db, task_id, scrap_data=_data.scrap_result, status=_data.status)
        if not updated_task:
            return ScrapResponse(success=False, message="Task not found with provided id", data=None)

        return ScrapResponse(
            success=True, message="Task updated successfully", data=updated_task.to_dict()
        )

    except Exception as e:
        logger.error(f"Error updating task data {e}", exc_info=True)
